# -*- coding: utf-8 -*-
"""
Parser for multipart/form-data
------------------------------

This module provides a parser for the multipart/form-data format. It can read
from a file, a socket or a WSGI environment. The parser can be used to replace
cgi.FieldStorage to work around its limitations.
"""


__author__ = "Marcel Hellkamp"
__version__ = "0.2.4"
__license__ = "MIT"
__all__ = ["MultipartError", "MultipartParser", "MultipartPart", "parse_form_data"]


import re
import sys
from io import BytesIO
from tempfile import TemporaryFile
from urllib.parse import parse_qs
from wsgiref.headers import Headers
from collections.abc import MutableMapping as DictMixin


##############################################################################
################################ Helper & Misc ###############################
##############################################################################
# Some of these were copied from bottle: https://bottlepy.org


# ---------
# MultiDict
# ---------


class MultiDict(DictMixin):
    """ A dict that remembers old values for each key.
        HTTP headers may repeat with differing values,
        such as Set-Cookie. We need to remember all
        values.
    """

    def __init__(self, *args, **kwargs):
        self.dict = dict()
        for k, v in dict(*args, **kwargs).items():
            self[k] = v

    def __len__(self):
        return len(self.dict)

    def __iter__(self):
        return iter(self.dict)

    def __contains__(self, key):
        return key in self.dict

    def __delitem__(self, key):
        del self.dict[key]

    def keys(self):
        return self.dict.keys()

    def __getitem__(self, key):
        return self.get(key, KeyError, -1)

    def __setitem__(self, key, value):
        self.append(key, value)

    def append(self, key, value):
        self.dict.setdefault(key, []).append(value)

    def replace(self, key, value):
        self.dict[key] = [value]

    def getall(self, key):
        return self.dict.get(key) or []

    def get(self, key, default=None, index=-1):
        if key not in self.dict and default != KeyError:
            return [default][index]

        return self.dict[key][index]

    def iterallitems(self):
        for key, values in self.dict.items():
            for value in values:
                yield key, value


def to_bytes(data, enc="utf8"):
    if isinstance(data, str):
        data = data.encode(enc)

    return data


def copy_file(stream, target, maxread=-1, buffer_size=2 ** 16):
    """ Read from :stream and write to :target until :maxread or EOF. """
    size, read = 0, stream.read

    while True:
        to_read = buffer_size if maxread < 0 else min(buffer_size, maxread - size)
        part = read(to_read)

        if not part:
            return size

        target.write(part)
        size += len(part)


# -------------
# Header Parser
# -------------


_special = re.escape('()<>@,;:"\\/[]?={} \t')
_re_special = re.compile(r'[%s]' % _special)
_quoted_string = r'"(?:\\.|[^"])*"'  # Quoted string
_value = r'(?:[^%s]+|%s)' % (_special, _quoted_string)  # Save or quoted string
_option = r'(?:;|^)\s*([^%s]+)\s*=\s*(%s)' % (_special, _value)
_re_option = re.compile(_option)  # key=value part of an Content-Type like header


def header_quote(val):
    if not _re_special.search(val):
        return val

    return '"' + val.replace("\\", "\\\\").replace('"', '\\"') + '"'


def header_unquote(val, filename=False):
    if val[0] == val[-1] == '"':
        val = val[1:-1]

        if val[1:3] == ":\\" or val[:2] == "\\\\":
            val = val.split("\\")[-1]  # fix ie6 bug: full path --> filename

        return val.replace("\\\\", "\\").replace('\\"', '"')

    return val


def parse_options_header(header, options=None):
    if ";" not in header:
        return header.lower().strip(), {}

    content_type, tail = header.split(";", 1)
    options = options or {}

    for match in _re_option.finditer(tail):
        key = match.group(1).lower()
        value = header_unquote(match.group(2), key == "filename")
        options[key] = value

    return content_type, options


##############################################################################
################################## Multipart #################################
##############################################################################


class MultipartError(ValueError):
    pass


class MultipartParser(object):
    def __init__(
        self,
        stream,
        boundary,
        content_length=-1,
        disk_limit=2 ** 30,
        mem_limit=2 ** 20,
        memfile_limit=2 ** 18,
        buffer_size=2 ** 16,
        charset="latin1",
    ):
        """ Parse a multipart/form-data byte stream. This object is an iterator
            over the parts of the message.

            :param stream: A file-like stream. Must implement ``.read(size)``.
            :param boundary: The multipart boundary as a byte string.
            :param content_length: The maximum number of bytes to read.
        """
        self.stream = stream
        self.boundary = boundary
        self.content_length = content_length
        self.disk_limit = disk_limit
        self.memfile_limit = memfile_limit
        self.mem_limit = min(mem_limit, self.disk_limit)
        self.buffer_size = min(buffer_size, self.mem_limit)
        self.charset = charset

        if self.buffer_size - 6 < len(boundary):  # "--boundary--\r\n"
            raise MultipartError("Boundary does not fit into buffer_size.")

        self._done = []
        self._part_iter = None

    def __iter__(self):
        """ Iterate over the parts of the multipart message. """
        if not self._part_iter:
            self._part_iter = self._iterparse()

        for part in self._done:
            yield part

        for part in self._part_iter:
            self._done.append(part)
            yield part

    def parts(self):
        """ Returns a list with all parts of the multipart message. """
        return list(self)

    def get(self, name, default=None):
        """ Return the first part with that name or a default value (None). """
        for part in self:
            if name == part.name:
                return part

        return default

    def get_all(self, name):
        """ Return a list of parts with that name. """
        return [p for p in self if p.name == name]

    def _lineiter(self):
        """ Iterate over a binary file-like object line by line. Each line is
            returned as a (line, line_ending) tuple. If the line does not fit
            into cls.buffer_size, line_ending is empty and the rest of the line
            is returned with the next iteration.
        """
        read = self.stream.read
        maxread, maxbuf = self.content_length, self.buffer_size
        buffer = b""  # buffer for the last (partial) line

        while True:
            data = read(maxbuf if maxread < 0 else min(maxbuf, maxread))
            maxread -= len(data)
            lines = (buffer + data).splitlines(True)
            len_first_line = len(lines[0])

            # be sure that the first line does not become too big
            if len_first_line > self.buffer_size:
                # at the same time don't split a '\r\n' accidentally
                if len_first_line == self.buffer_size + 1 and lines[0].endswith(b"\r\n"):
                    splitpos = self.buffer_size - 1
                else:
                    splitpos = self.buffer_size
                lines[:1] = [lines[0][:splitpos], lines[0][splitpos:]]

            if data:
                buffer = lines[-1]
                lines = lines[:-1]

            for line in lines:
                if line.endswith(b"\r\n"):
                    yield line[:-2], b"\r\n"
                elif line.endswith(b"\n"):
                    yield line[:-1], b"\n"
                elif line.endswith(b"\r"):
                    yield line[:-1], b"\r"
                else:
                    yield line, b""

            if not data:
                break

    def _iterparse(self):
        lines, line = self._lineiter(), ""
        separator = b"--" + to_bytes(self.boundary)
        terminator = b"--" + to_bytes(self.boundary) + b"--"

        # Consume first boundary. Ignore any preamble, as required by RFC
        # 2046, section 5.1.1.
        for line, nl in lines:
            if line in (separator, terminator):
                break
        else:
            raise MultipartError("Stream does not contain boundary")

        # Check for empty data
        if line == terminator:
            for _ in lines:
                raise MultipartError("Data after end of stream")
            return

        # For each part in stream...
        mem_used, disk_used = 0, 0  # Track used resources to prevent DoS
        is_tail = False  # True if the last line was incomplete (cutted)

        opts = {
            "buffer_size": self.buffer_size,
            "memfile_limit": self.memfile_limit,
            "charset": self.charset,
        }

        part = MultipartPart(**opts)

        for line, nl in lines:
            if line == terminator and not is_tail:
                part.file.seek(0)
                yield part
                break

            elif line == separator and not is_tail:
                if part.is_buffered():
                    mem_used += part.size
                else:
                    disk_used += part.size
                part.file.seek(0)

                yield part

                part = MultipartPart(**opts)

            else:
                is_tail = not nl  # The next line continues this one
                try:
                    part.feed(line, nl)

                    if part.is_buffered():
                        if part.size + mem_used > self.mem_limit:
                            raise MultipartError("Memory limit reached.")
                    elif part.size + disk_used > self.disk_limit:
                        raise MultipartError("Disk limit reached.")
                except MultipartError:
                    part.close()
                    raise
        else:
            # If we run off the end of the loop, the current MultipartPart
            # will not have been yielded, so it's our responsibility to
            # close it.
            part.close()

        if line != terminator:
            raise MultipartError("Unexpected end of multipart stream.")


class MultipartPart(object):
    def __init__(self, buffer_size=2 ** 16, memfile_limit=2 ** 18, charset="latin1"):
        self.headerlist = []
        self.headers = None
        self.file = False
        self.size = 0
        self._buf = b""
        self.disposition = None
        self.name = None
        self.filename = None
        self.content_type = None
        self.charset = charset
        self.memfile_limit = memfile_limit
        self.buffer_size = buffer_size

    def feed(self, line, nl=""):
        if self.file:
            return self.write_body(line, nl)

        return self.write_header(line, nl)

    def write_header(self, line, nl):
        line = line.decode(self.charset)

        if not nl:
            raise MultipartError("Unexpected end of line in header.")

        if not line.strip():  # blank line -> end of header segment
            self.finish_header()
        elif line[0] in " \t" and self.headerlist:
            name, value = self.headerlist.pop()
            self.headerlist.append((name, value + line.strip()))
        else:
            if ":" not in line:
                raise MultipartError("Syntax error in header: No colon.")

            name, value = line.split(":", 1)
            self.headerlist.append((name.strip(), value.strip()))

    def write_body(self, line, nl):
        if not line and not nl:
            return  # This does not even flush the buffer

        self.size += len(line) + len(self._buf)
        self.file.write(self._buf + line)
        self._buf = nl

        if self.content_length > 0 and self.size > self.content_length:
            raise MultipartError("Size of body exceeds Content-Length header.")

        if self.size > self.memfile_limit and isinstance(self.file, BytesIO):
            # TODO: What about non-file uploads that exceed the memfile_limit?
            self.file, old = TemporaryFile(mode="w+b"), self.file
            old.seek(0)
            copy_file(old, self.file, self.size, self.buffer_size)

    def finish_header(self):
        self.file = BytesIO()
        self.headers = Headers(self.headerlist)
        content_disposition = self.headers.get("Content-Disposition", "")
        content_type = self.headers.get("Content-Type", "")

        if not content_disposition:
            raise MultipartError("Content-Disposition header is missing.")

        self.disposition, self.options = parse_options_header(content_disposition)
        self.name = self.options.get("name")
        self.filename = self.options.get("filename")
        self.content_type, options = parse_options_header(content_type)
        self.charset = options.get("charset") or self.charset
        self.content_length = int(self.headers.get("Content-Length", "-1"))

    def is_buffered(self):
        """ Return true if the data is fully buffered in memory."""
        return isinstance(self.file, BytesIO)

    @property
    def value(self):
        """ Data decoded with the specified charset """

        return self.raw.decode(self.charset)

    @property
    def raw(self):
        """ Data without decoding """
        pos = self.file.tell()
        self.file.seek(0)

        try:
            val = self.file.read()
        except IOError:
            raise
        finally:
            self.file.seek(pos)

        return val

    def save_as(self, path):
        with open(path, "wb") as fp:
            pos = self.file.tell()

            try:
                self.file.seek(0)
                size = copy_file(self.file, fp)
            finally:
                self.file.seek(pos)

        return size

    def close(self):
        if self.file:
            self.file.close()
            self.file = False


##############################################################################
#################################### WSGI ####################################
##############################################################################


def parse_form_data(environ, charset="utf8", strict=False, **kwargs):
    """ Parse form data from an environ dict and return a (forms, files) tuple.
        Both tuple values are dictionaries with the form-field name as a key
        (unicode) and lists as values (multiple values per key are possible).
        The forms-dictionary contains form-field values as unicode strings.
        The files-dictionary contains :class:`MultipartPart` instances, either
        because the form-field was a file-upload or the value is too big to fit
        into memory limits.

        :param environ: An WSGI environment dict.
        :param charset: The charset to use if unsure. (default: utf8)
        :param strict: If True, raise :exc:`MultipartError` on any parsing
                       errors. These are silently ignored by default.
    """

    forms, files = MultiDict(), MultiDict()

    try:
        if environ.get("REQUEST_METHOD", "GET").upper() not in ("POST", "PUT"):
            raise MultipartError("Request method other than POST or PUT.")
        content_length = int(environ.get("CONTENT_LENGTH", "-1"))
        content_type = environ.get("CONTENT_TYPE", "")

        if not content_type:
            raise MultipartError("Missing Content-Type header.")

        content_type, options = parse_options_header(content_type)
        stream = environ.get("wsgi.input") or BytesIO()
        kwargs["charset"] = charset = options.get("charset", charset)

        if content_type == "multipart/form-data":
            boundary = options.get("boundary", "")

            if not boundary:
                raise MultipartError("No boundary for multipart/form-data.")

            for part in MultipartParser(stream, boundary, content_length, **kwargs):
                if part.filename or not part.is_buffered():
                    files[part.name] = part
                else:  # TODO: Big form-fields are in the files dict. really?
                    forms[part.name] = part.value

        elif content_type in (
            "application/x-www-form-urlencoded",
            "application/x-url-encoded",
        ):
            mem_limit = kwargs.get("mem_limit", 2 ** 20)
            if content_length > mem_limit:
                raise MultipartError("Request too big. Increase MAXMEM.")

            data = stream.read(mem_limit).decode(charset)

            if stream.read(1):  # These is more that does not fit mem_limit
                raise MultipartError("Request too big. Increase MAXMEM.")

            data = parse_qs(data, keep_blank_values=True, encoding=charset)

            for key, values in data.items():
                for value in values:
                    forms[key] = value
        else:
            raise MultipartError("Unsupported content type.")

    except MultipartError:
        if strict:
            for part in files.values():
                part.close()
            raise

    return forms, files

"""
Data objects or wrappers used by the api module.
"""

import os
from json import JSONDecodeError

import requests
from requests_toolbelt import MultipartEncoder

from pycdstar3._utils import PATH_TYPES


class JsonObject(dict):
    """A custom dict class that allows attribute access to values."""

    def __getattr__(self, item):
        return self.get(item)


class FileDownload:
    """Wrapper for streamed file downloads.

    The file content can only be read once.
    """

    def __init__(self, vault, archive, name, rs: requests.Response):
        self.vault = vault
        self.archive = archive
        self.name = name
        self.response = rs
        self.read = rs.raw.read

    @property
    def basename(self):
        return os.path.basename(self.name)

    @property
    def type(self):
        return self.response.headers["Content-Type"]

    @property
    def is_partial(self):
        return self.response.status_code == 206

    @property
    def size(self):
        return int(self.response.headers["Content-Length"])

    def __iter__(self):
        """Iterate over chunks of data (NOT lines)"""
        return self.iter_content()

    def iter_content(self, buffsize=1024 * 64):
        """Iterate over chunks of data (NOT lines)"""
        return self.response.iter_content(chunk_size=buffsize)

    def save_as(self, target, overwrite=False):
        """Save this download to a file (str, Path or file-like)"""
        if not hasattr(target, "write"):
            with open(target, "wb" if overwrite else "xb") as fp:
                return self.save_as(fp)
        for chunk in self.iter_content():
            target.write(chunk)

    def save_to(self, dest, keep_path=False, overwrite=False):
        """Save this download to a directory."""
        dest = os.path.abspath(dest)
        if not os.path.isdir(dest):
            raise IOError("Not a directory: " + dest)
        target = os.path.join(dest, self.name if keep_path else self.basename)
        if target != os.path.normpath(target):
            raise IOError("Would escape target directory: " + target)

        os.makedirs(os.path.dirname(target), exist_ok=True)
        self.save_as(target, overwrite=overwrite)

    def close(self):
        self.response.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __repr__(self):
        return "FileDownload({}/{} name={!r} size={})".format(
            self.vault, self.archive, self.name, self.size
        )

    def readall(self):
        """Read the entire download into memory and return a single large byte object."""
        return self.response.content


class FormUpdate:
    """Builder for CDSTAR POST multipart/form-data requests to upload multiple files or
    change aspects of an archive.
    """

    def __init__(self):
        self.fields = []
        self._mp = None

    def _rm(self, key):
        self.fields[:] = [f for f in self.fields if f[0] != key]

    @property
    def body(self):
        if not self._mp:
            self._mp = MultipartEncoder(self.fields)
        return self._mp

    @property
    def content_type(self):
        return self.body.content_type

    def upload(self, name, src, type="application/x-autodetect"):
        """Upload a file (string path or opened file-like object)

        :param target: Target within the archive (must start with '/')
        :param src: String path to an existing file, or opened file-like object.
        :param type: Mime-type of the upload.
        :return: self
        """
        if not name.startswith("/"):
            name = "/" + name
        if isinstance(src, PATH_TYPES):
            # TODO: Check what types are accepted as file-like and build a lazily opened
            #       wrapper.
            self.fields.append((name, (os.path.basename(src), open(src, "rb"), type)))
        elif hasattr(src, "fileno") or hasattr(src, "getvalue"):
            self.fields.append((name, (os.path.basename(src), src, type)))
        else:
            raise ValueError(
                "Source must be a file path (str), byte buffer or opened file"
            )
        return self

    def acl(self, subject, *permissions):
        """Set permissions for a subject. Existing permissions for the same subject are
        replaced.

        :param subject: A subject-name, @groupname or one of `$any`, `$user`, `$user`
        :param permissions:
        :return: self
        """

        # TODO: Check for valid subject and permission names
        sub = "acl:{}".format(subject)
        self._rm(sub)
        self.fields.append((sub, ",".join(permissions)))
        return self

    def meta(self, field, *values, file=None):
        """
        Set metadata for the archive, or a file within the archive.

        :param field: Meta-attribute field name. Should start with a schema prefix
                    (e.g. `dc:` for DublinCore)
        :param values: Values for this meta attribute.
        :param file: File name to attach the metadata to. If not set, it is assigned to
                     the entire archive.
        :return: self
        """

        attr = "meta:" + field
        if file:
            attr += ":/" + file.lstrip("/")

        self._rm(attr)

        if values:
            for val in values:
                self.fields.append((attr, val))
        else:
            self._rm(attr)
            self.fields.append((attr, ""))

        return self

    def profile(self, name):
        """
        Set archive profile to a new value.

        :param name: Profile name.
        :return: self
        """

        self._rm("profile")
        self.fields.append(("profile", name))

        return self


class ApiError(Exception):
    def __init__(self, rs):
        if rs.ok:
            raise AssertionError("Not an error response: " + repr(rs))

        self.rs = rs
        try:
            self.json = rs.json()
        except JSONDecodeError:
            raise ValueError(
                "Failed to decode server response (invalid JSON):"
                " {0.method} {0.url} ->"
                " {1.status_code} ({1.headers[content-type]})".format(rs.request, rs)
            )

    @property
    def error(self):
        return self.json["error"]

    @property
    def message(self):
        return self.json["message"]

    @property
    def status(self):
        return self.json["status"]

    @property
    def detail(self):
        return self.json.get("detail") or {}

    def __repr__(self):
        return "{0.error}({0.status}): {0.message}".format(self)

    __str__ = __repr__

    def pretty(self):
        err = "API Error: {} ({})\n".format(self.error, self.status)
        err += "Message: {}\n".format(self.message)
        if self.detail:
            err += "Details:\n"
            for k, v in self.detail:
                err += "  {}: {!r}\n".format(k, v)
        return err

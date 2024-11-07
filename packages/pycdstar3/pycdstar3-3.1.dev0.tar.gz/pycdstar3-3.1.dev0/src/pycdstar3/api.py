"""
Client api implementation. Usually imported directly from :mod:`pycdstar` and not from
here.
"""

import os
import threading
import typing

import requests

from pycdstar3._utils import PATH_TYPES, url_split_auth, IntervalTimer
from pycdstar3.model import ApiError, JsonObject, FileDownload, FormUpdate

__all__ = "CDStar", "CDStarVault", "FormUpdate", "ApiError"


class CDStar:
    """Provide low-level methods for corresponding server-side REST endpoints.

    If not documented otherwise, each method call triggers exactly one REST request
    and return a :class:`pycdstar3.model.JsonObject`, which offers dict-like and
    attribute access to json fields. There is no internal caching. The only state
    that is tracked by this class is the running transaction, if any.

    :param url: CDSTAR API URL, with or without auth information
    :param auth: A (username, password) tuple, or None.
    """

    def __init__(self, url, auth=None, _session=None):
        url, username, password = url_split_auth(url)
        if not url.endswith("/"):
            url += "/"
        self.url = url
        self.auth = auth or username and (username, password)

        self._session = _session or requests.Session()
        self._tx = None
        self._autocommit = False
        self._keepalive_timer = None

    def clone(self):
        """Return an independent instance with the same settings.

        Other state (e.g. running transaction) is not copied.
        """
        return CDStar(self.url, auth=self.auth, _session=self._session)

    def raw(self, method, *path, expect_status=None, **options) -> requests.Response:
        """Send a raw HTTP request to the cdstar server and return a raw response.

        Authentication and transaction headers are added automatically.
        Error responses are thrown as `ApiError`, unless the status code is
        explicitly accepted as valid via `expect_status`.

        Disclaimer: Avoid using this method if there is a more specific
        implementation available. If you find a feature missing from this class,
        please submit a feature request instead of over-using this method.
        """

        if self.auth:
            options["auth"] = self.auth

        if self.tx:
            options.setdefault("headers", {})["X-Transaction"] = self.tx["id"]

        path = [requests.utils.quote(p) for p in path]

        rs = self._session.request(method, self.url + "/".join(path), **options)

        if rs.ok or (expect_status and rs.status_code in expect_status):
            return rs

        raise ApiError(rs)

    def rest(
        self, method, *path, expect_status=None, **options
    ) -> typing.Optional[JsonObject]:
        """Just like `raw()`, but expects the response to be JSON and returns
        the parsed result instead of the raw response. Non-JSON responses
        are errors. Empty (204) responses return None.

        Disclaimer: Avoid using this method if there is a more specific
        implementation available. If you find a feature missing from this class,
        please submit a feature request instead of over-using this method.
        """

        # TODO: Expect json errors or non-json responses and
        # throw a better error message
        rs = self.raw(method, *path, expect_status=expect_status, **options)
        if rs.status_code == 204:
            return None
        return rs.json(object_hook=JsonObject)

    def begin(self, autocommit=False, readonly=False, keepalive=False):
        """Start a new transaction and return self.

        Transactions are used to group multiple operations into a single atomic
        action. After begin(), you have to call commit() or rollback() to apply
        or undo all operations made while the transaction was active.

        It is strongly recommended to always wrap transactions in with-blocks::

            with cdstar.begin():
                # do stuff

        You can commit() or rollback() early, or even begin() a new transaction
        while still in the with-block, but there can only be a single transaction
        per client active at a time. On exit, the current transaction is closed
        automatically. If autocommit is true and no exception was raised,
        it is committed. Otherwise, it is rolled back.

        :param autocommit: Commit this transaction if the with-block ended without
                           errors. (default: False)
        :param readonly: Create a (cheaper) read-only transaction. (default: False)
        :param keepalive: Automatically call :meth:`keepalive` from a separate
                          thread. This is only required when waiting for user input
                          for a long time. (default: False)
        """
        self.rollback()
        self._autocommit = autocommit
        self._tx = self.rest("POST", "_tx", data={"readonly": readonly})
        if keepalive:
            self._auto_keepalive_start()
        return self

    @property
    def tx(self) -> JsonObject | None:
        """Return the transaction handle, or None if no transaction is running."""
        return self._tx

    def commit(self):
        """Commit the current transaction."""
        if not self._tx:
            raise RuntimeError("No transaction running")
        self._auto_keepalive_stop()

        try:
            self.raw("POST", "_tx", self._tx.id)
            self._tx = None
        except Exception:
            self.rollback()
            raise

    def rollback(self):
        """Rollback the current transaction, if any. Do nothing otherwise."""
        self._auto_keepalive_stop()

        try:
            if self._tx:
                self.raw("DELETE", "_tx", self._tx["id"])
        finally:
            self._tx = None

    def keepalive(self):
        """Keep the current transaction alive (reset the timeout)."""
        if not self._tx:
            raise RuntimeError("No transaction running")
        self._tx = self.rest("POST", "_tx", self._tx["id"], params={"renew": True})

    def _auto_keepalive_start(self):
        self._auto_keepalive_stop()
        # leeway: 10% or 2 seconds, but sleep for at least a second
        interval = max(1, min(self.tx["ttl"] * 0.9, self.tx["ttl"] - 2))
        self._keepalive_timer = IntervalTimer(interval, self._auto_keepalive, self.tx)
        self._keepalive_timer.daemon = True
        self._keepalive_timer.start()

    def _auto_keepalive(self, tx):
        timer = self._keepalive_timer
        if timer != threading.current_thread():
            raise RuntimeError()
        if not self.tx or self.tx["id"] != tx["id"]:
            raise RuntimeError()

        self.keepalive()

        # leeway: 10% or 2 seconds, but sleep for at least a second
        timer.set_interval(max(1, min(self.tx["ttl"] * 0.9, self.tx["ttl"] - 2)))

    def _auto_keepalive_stop(self):
        """Stop the current keepalive timer, if any."""
        if self._keepalive_timer:
            self._keepalive_timer.cancel()
            self._keepalive_timer = None

    def __enter__(self):
        """Expect a transaction to be already running."""
        if not self._tx:
            raise RuntimeError("No transaction running. Call begin() frist.")

    def __exit__(self, exc_type, exc_value, traceback):
        """Commit or roll-back the current transaction (see autocommit)"""
        if self._tx:
            if exc_type is None and self._autocommit:
                self.commit()
            else:
                self.rollback()

    def exists(self, vault, archive=None, file=None) -> bool:
        """Checks if a vault, archive or file exists"""
        if file is not None:
            return self.raw("HEAD", vault, archive, file, expect_status=[200, 404]).ok
        elif archive is not None:
            return self.raw("HEAD", vault, archive, expect_status=[200, 404]).ok
        else:
            return self.raw("HEAD", vault, expect_status=[200, 404]).ok

    def service_info(self) -> JsonObject:
        """Get information about the cdstar service instance"""
        return self.rest("GET")

    def vault_info(self, vault: str) -> JsonObject:
        """Get information about a vault"""
        return self.rest("GET", vault)

    def create_archive(self, vault, form: FormUpdate = None) -> JsonObject:
        """Create a new archive."""
        if form:
            return self.rest(
                "POST",
                vault,
                data=form.body,
                headers={"Content-Type": form.content_type},
            )
        else:
            return self.rest("POST", vault)

    def update_archive(self, vault, archive, form: FormUpdate) -> JsonObject:
        """Update an existing archive"""
        return self.rest(
            "POST",
            vault,
            archive,
            data=form.body,
            headers={"Content-Type": form.content_type},
        )

    def archive_info(self, vault, archive, meta=False, files=False) -> JsonObject:
        """Get information about an archive"""
        query = {"info": "true"}
        if meta:
            query.setdefault("with", []).append("meta")
        if files:
            query.setdefault("with", []).append("files")
        return self.rest("GET", vault, archive, params=query)

    def delete_archive(self, vault, archive) -> bool:
        """Remove an archive. This cannot be undone."""
        return self.raw("DELETE", vault, archive).ok

    def put_file(
        self, vault, archive, name, source, type=None, replace=True
    ) -> JsonObject:
        """Create or replace a single file on an existing archive.

        If the file exists remotely and `replace=True` is set (default), the file
        content is overridden but everything else (metadata, type, file id) stays the
        same. If `replace` is `False` then a file name conflict is an error.

        :param vault: Vault name
        :param archive: Archive ID
        :param name: Target file name. May start with `/` (optional).
        :param source: Readable file, byte buffer or iterator, or a file path that will
                       then be opened in 'rb' mode.
        :param type: Mime-type to set on the uploaded file. (default: guess)
        :param replace: Replace existing remote files (default: True)
        :return:
        """

        if isinstance(source, PATH_TYPES):
            with open(source, "rb") as source:
                return self.put_file(
                    vault, archive, name, source, type=type, replace=replace
                )

        headers = {"Content-Type": type or "application/x-autodetect"}
        if not replace:
            headers["If-None-Match"] = "*"

        return self.rest(
            "PUT", vault, archive, _fix_filename(name), data=source, headers=headers
        )

    def get_file(self, vault, archive, name, offset=0) -> FileDownload:
        """Request a file and return a stream-able :class:`FileDownload`.

        The request is issued with `stream=True`, which means it is still open and
        not fully read when this method returns. The returned wrapper MUST be
        `close()`d after use, or wrapped in a `with` statement::

            with cdstar.get_file(vault, id, "/file/name.txt") as dl:
                dl.save_to("~/Downloads/")

        """
        headers = {"Range": "bytes={}-".format(offset)} if offset > 0 else {}
        name = _fix_filename(name)
        rs = self.raw("GET", vault, archive, name, stream=True, headers=headers)
        return FileDownload(vault, archive, name, rs)

    def file_info(self, vault, archive, name, meta=False) -> JsonObject:
        """Get information about a file"""
        query = {"info": "true"}
        if meta:
            query["with"] = "meta"
        return self.rest("GET", vault, archive, _fix_filename(name), params=query)

    def list_files(
        self,
        vault,
        archive,
        offset=0,
        limit=100,
        meta=False,
        order=None,
        reverse=False,
        include_glob=None,
        exclude_glob=None,
    ) -> JsonObject:
        """Request a FileList for an archive.

        The FileList may be incomplete of more than `limit` files are in an archive.
        See iter_files() for a convenient way to get all files as an iterator.
        """

        query = {"files": "true", "offset": offset, "limit": limit}
        if include_glob:
            query["include"] = include_glob
        if exclude_glob:
            query["exclude"] = exclude_glob
        if meta:
            query["with"] = "meta"
        if order:
            query["order"] = order
        if reverse:
            query["reverse"] = "True"

        return self.rest("GET", vault, archive, params=query)

    def iter_files(
        self, vault, archive, offset=0, **args
    ) -> typing.Iterator[JsonObject]:
        """Yield all FileInfo entries of an archive.

        This method may (lazily) issue more than one request if an archive contains
        more than `limit` files.
        """

        while True:
            files = self.list_files(vault, archive, offset, **args)
            if files["files"] and offset + files["count"] <= files["total"]:
                yield from files["files"]
                offset += files["count"]
            else:
                break

    def delete_file(self, vault, archive, file) -> bool:
        """Remove a archive file. This cannot be undone."""
        return self.raw("DELETE", vault, archive, file).ok

    def acl_info(self, vault, archive, explode=False) -> JsonObject:
        """Get the access control list (ACL) for an archive."""
        mode = "explode" if explode else "group"
        return self.rest("GET", vault, archive, params={"acl": mode})

    def set_acl(self, vault, archive, acl_info) -> JsonObject:
        """Set (replace) the access control list (ACL) for an archive"""
        return self.rest("PUT", vault, archive, params={"acl": ""}, json=acl_info)

    def meta_info(self, vault, archive, file=None) -> JsonObject:
        """Get the metadata of an archvie or file."""
        if file:
            return self.rest("GET", vault, archive, file, params={"meta": ""})
        return self.rest("GET", vault, archive, params={"meta": ""})

    def scroll(self, vault, start="", limit=1024, strict=False) -> JsonObject:
        """List IDs in a vault.

        By default, all IDs that were ever created in that vault are
        returned, including deleted or private archives. This requires
        `list` permissions on the vault.

        In strict mode (since 3.0.4) only archives load-able by the current
        user are considered.
        """
        params = {"scroll": start, "limit": limit}
        if strict:
            params["strict"] = strict
        return self.rest("GET", vault, params=params)

    def iter_scroll(
        self, vault, start="", limit=1024, strict=False
    ) -> typing.Iterator[JsonObject]:
        while True:
            page = self.scroll(vault, start=start, limit=limit, strict=strict)
            if not page["results"]:
                break
            yield from page["results"]
            start = page["results"][-1]
            if page["count"] < page["limit"]:
                break

    def search(
        self, vault, q, order=None, limit=0, scroll=None, groups=None
    ) -> JsonObject:
        """Perform a search and return a single page of search results.

        See iter_search() for a convenient way to fetch more than `limit` results.
        """
        params = {"q": q}
        if order:
            params["order"] = order
        if limit:
            params["limit"] = limit
        if scroll:
            params["scroll"] = scroll
        if groups:
            params["groups"] = groups
        return self.rest("GET", vault, params=params)

    def iter_search(self, vault, q, scroll=None, **args) -> typing.Iterator[JsonObject]:
        """Yield all search hits of a search.

        This method may (lazily) issue more than one request if a search returns
        more than `limit` results.
        """
        while True:
            page = self.search(vault, q, scroll=scroll or "", **args)
            if page["hits"]:
                yield from page["hits"]
                scroll = page["scroll"]
            else:
                break


def _fix_filename(name):
    """Normalize a remote archive file path and make sure it makes sense.

    Raise if we find relative path segments (likely an error)
    """
    # silently strip leading slashes
    name = name.lstrip("/")

    # Fail hard on relative filenames
    if name != os.path.normpath(name):
        raise ValueError(
            "Archive file name not in a normalized form: {} != {}".format(
                name, os.path.normpath(name)
            )
        )
    return name


# Design notes for the following resource handles:
# - The handle instances are really just a slim handle for a remote resource, NOT a
#   wrapper, local copy or cache. They should not cache or store anything that might
#   change remotely.
# - Only methods are allowed to trigger requests, preferably only one request per call.
# - Handles MUST implement exists()->bool and info()->JsonObject.


class CDStarVault:
    """Fluent API handle for a CDSTAR vault.

    This is just a thin wrapper to provide a more fluent and object-oriented API on
    top of :class:`CDStar`. No remote state is cached locally and most method calls
    will trigger REST requests.
    """

    __slots__ = "api", "name"

    def __init__(self, api: CDStar, vault: str):
        if not api or not vault:
            raise AssertionError("Parameters must not be none")
        self.api = api
        self.name = vault

    def exists(self):
        """Checks if a vault exists"""
        return self.api.exists(self.name)

    def info(self) -> JsonObject:
        """Get information about a vault"""
        return self.api.vault_info(self.name)

    def new_archive(self, *a, **ka) -> "CDStarArchive":
        """Create a new archive and return a handle to it."""
        return CDStarArchive(self, self.api.create_archive(self.name, *a, **ka).id)

    def archive(self, id: str) -> "CDStarArchive":
        """Return a handle for a specific archive in this vault.

        The archive may or may not exist remotely. Check with `exist()`.
        """
        return CDStarArchive(self, id)

    def search(self, *a, **ka) -> JsonObject:
        """Search in this vault. Return a single result page."""
        return self.api.search(self.name, *a, **ka)

    def iter_search(self, *a, **ka) -> typing.Iterator[JsonObject]:
        """Search in this vault.

        Return a result iterator, which lazily issues more requests on demand."""
        return self.api.iter_search(self.name, *a, **ka)


class CDStarArchive:
    """Handle for a CDSTAR archive.

    See :class:`CDStarVault` for details on how handles work.
    """

    __slots__ = "api", "vault", "id"

    def __init__(self, vault: CDStarVault, archive_id):
        if not vault or not archive_id:
            raise AssertionError("Parameters must not be none")
        self.api = vault.api
        self.vault = vault
        self.id = archive_id

    def exists(self):
        """Checks if this archive exists."""
        return self.api.exists(self.vault.name, self.id)

    def delete(self):
        """Delete this archive."""
        return self.api.delete_archive(self.vault.name, self.id)

    def file(self, name: str) -> "CDStarFile":
        """Return a file handle.

        The file may or may not exist remotely. Check with `exist()`.
        """
        return CDStarFile(self, name)

    # TODO: Implement meee


class CDStarFile:
    """Handle for a CDSTAR file.

    See :class:`CDStarVault` for details on how handles work.
    """

    __slots__ = "api", "archive", "name"

    def __init__(self, archive: CDStarArchive, name: str):
        if not archive or not name:
            raise AssertionError("Parameters must not be none")
        self.api = archive.api
        self.archive = archive
        self.name = name

    def exists(self):
        """Checks if this file exists"""
        return self.api.exists(self.archive.vault.name, self.archive.id, self.name)

    def delete(self):
        """Delete this file from the archive."""
        return self.api.delete_file(self.archive.vault.name, self.archive.id, self.name)

    def put(self, **ka) -> JsonObject:
        """Create or overwrite file content"""
        return self.api.put_file(
            self.archive.vault.name, self.archive.id, self.name, **ka
        )

    def stream(self, **ka) -> FileDownload:
        """Request file content as a stream-able :class:`FileDownload`."""
        return self.api.get_file(
            self.archive.vault.name, self.archive.id, self.name, **ka
        )

    # TODO: Implement meee

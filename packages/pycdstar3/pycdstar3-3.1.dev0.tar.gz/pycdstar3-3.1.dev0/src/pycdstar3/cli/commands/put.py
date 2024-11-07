"""
Create or modify an archive.

Upload files and change other aspects of an archive, optionally creating it first.

Existing remote files are not overwritten by default to prevent accidental data
loss. The command will fail if there are any file name conflicts. To change that,
you can --force, --update or --skip conflicting files instead. Note that
--update will overwrite remote files based on modification time.

All uploads and changes are wrapped in a transaction. If something goes wrong,
nothing is committed on remote side and you can simply re-run the same command.

"""

import os
from contextlib import ExitStack

from pycdstar3 import FormUpdate
from pycdstar3.cli import CliError
from pycdstar3.cli._utils import hbytes, KvArgType, globtype
import collections
import iso8601


def register(subparsers):
    parser = subparsers.add_parser(
        "put", help=__doc__.strip().splitlines()[0], description=__doc__
    )

    _grp = parser.add_mutually_exclusive_group()
    _grp.add_argument(
        "-s", "--skip", action="store_true", help="Skip files that exist remotely."
    )
    _grp.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Update remote files if local file is newer, skip others.",
    )
    _grp.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Always overwrite remote files. (default: skip)",
    )

    # parser.add_argument("--delete", action="store_true",
    #                     help="Delete remote files not present locally,"
    #                          " if they match a PATH parameter.")
    parser.add_argument(
        "-i",
        "--include",
        metavar="GLOB",
        type=globtype,
        action="append",
        help="Include files by glob pattern (default: all)",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        metavar="GLOB",
        type=globtype,
        action="append",
        help="Exclude files by glob pattern",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files (default: skip)",
    )

    parser.add_argument(
        "--prefix",
        metavar="PREFIX",
        default="/",
        help="Upload files to this remote directory. (default: `/`)",
    )
    parser.add_argument(
        "--flat",
        action="store_true",
        help="Strip local directory names and only use the basename when uploading"
        " files. (e.g. ./path/to/file.txt would be uploaded as /file.txt)",
    )

    parser.add_argument(
        "--meta",
        metavar="KEY=VAL",
        type=KvArgType("="),
        action="append",
        help="Set archive metadata attributes. An empty value removes the attribute."
        " Can be repeated to set multiple values for the same attribute.",
    )
    parser.add_argument(
        "--acl",
        metavar="SUBJECT=ALLOW",
        type=KvArgType("="),
        action="append",
        help="Set archive level permissions for a subject. ALLOW can be a "
        "comma-separated list of permission or permission-set names. "
        "Leave the ALLOW part empty to revoke all permissions for a subject.",
    )
    parser.add_argument(
        "--profile",
        metavar="NAME",
        help="Change archive profile.",
    )

    parser.add_argument(
        "-n",
        "--dry-run",
        action="store_true",
        help="Just simulate an upload and print what would have been done.",
    )
    parser.add_argument(
        "-%", "--progress", action="store_true", help="Show progress bar."
    )

    parser.add_argument("ARCHIVE", help="Archive ID, or 'new' to create a new archive")
    parser.add_argument("PATH", nargs="*", help="Files or directories to upload.")
    parser.set_defaults(main=command)


def collect_files(path, hidden=False):
    if os.path.isfile(path):
        yield path
    elif os.path.isdir(path):
        for root, dlist, flist in os.walk(path):
            if not hidden:
                dlist[:] = [name for name in dlist if not name.startswith(".")]
                flist[:] = [name for name in flist if not name.startswith(".")]
            yield from (os.path.join(root, name) for name in flist)
    else:
        raise CliError("Not a file: " + path)


def remote_name(base, file, prefix="", flatten=False):
    target = os.path.relpath(file, base)
    if flatten:
        target = os.path.basename(target)
    if prefix:
        target = os.path.join(prefix, target)
    if target != os.path.normpath(target):
        raise CliError("Unable to upload relative path: {!r}".format(target))
    return target


UploadTask = collections.namedtuple("UploadTask", "local remote stats")


def command(ctx, args):  # noqa: C901
    client = ctx.client
    vault = ctx.vault
    archive = args.ARCHIVE

    prefix = args.prefix
    prefix = prefix.lstrip("/")

    inc_rules = args.include or []
    exc_rules = args.exclude or []

    dryrun = "[dryrun] " if args.dry_run else ""

    # Collect meta changes
    meta = {}
    for key, split, val in args.meta or []:
        # TODO: Support += and -= as well as @ to load from files
        meta.setdefault(key, []).append(val)

    # Collect ACL changes
    acl = {}
    for key, split, val in args.acl or []:
        # TODO: Support += and -=
        acl.setdefault(key, []).append(val)

    # Collect files to upload
    uploads = {}
    for path in args.PATH:
        for file in collect_files(path, args.include_hidden):
            if inc_rules and not any(rule.match(file) for rule in inc_rules):
                ctx.print.v("Not included: {}", file)
            elif any(rule.match(file) for rule in exc_rules):
                ctx.print.v("Excluded: {}", file)
            else:
                fstat = os.stat(file)
                rname = remote_name(".", file, prefix, args.flat)
                task = UploadTask(file, rname, fstat)
                if rname in uploads:
                    a, b = uploads[rname].local, task.local
                    msg = "Conflicting uploads: Both {!r} and {!r} map to {!r}"
                    raise CliError(msg.format(a, b, rname))
                uploads[rname] = task

    with ExitStack() as stack:
        if not dryrun:
            stack.enter_context(client.begin(autocommit=True))

        # Create archive if necessary, or check if it exists
        created = False
        if archive == "new":
            if not dryrun:
                archive = client.create_archive(vault)["id"]
            ctx.print("{}Created new archive: {}", dryrun, archive)
            created = True
        elif not client.exists(vault, archive):
            raise CliError("Archive does not exist: {}".format(archive))

        # In any but --force mode, check for upload conflicts
        if uploads and not created and not args.force:
            ctx.print.v("Fetching remote file list...")
            for remote in client.iter_files(vault, archive):
                rname = remote["name"]
                if rname not in uploads:
                    continue
                if args.skip:
                    ctx.print.v("Skipping (--skip): {}", rname)
                    del uploads[rname]
                elif args.update:
                    lmtime = uploads[rname].stats.st_mtime
                    rmtime = iso8601.parse_date(remote["modified"]).timestamp()
                    if lmtime <= rmtime:
                        ctx.print.v("Skipping (--update): {}", rname)
                        del uploads[rname]
                else:
                    msg = "Remote file exists: {!r}\n".format(rname)
                    msg += "Enable --force, --update or --skip and try again."
                    raise CliError(msg)

        if meta:
            ctx.print("{}Updating archive metadata ...", dryrun)
            form = FormUpdate()
            for key, values in meta.items():
                form.meta(key, *values)
            if not dryrun:
                client.update_archive(vault, archive, form=form)

        if acl:
            ctx.print("{}Updating archive ACL ...", dryrun)
            form = FormUpdate()
            for key, values in acl.items():
                form.acl(key, *values)
            if not dryrun:
                client.update_archive(vault, archive, form=form)

        if args.profile:
            ctx.print("{}Updating archive profile ...", dryrun)
            form = FormUpdate()
            form.profile(args.profile or "default")
            if not dryrun:
                client.update_archive(vault, archive, form=form)

        # Early exit if we do not have any files to upload
        if not uploads:
            ctx.print("{}Done!", dryrun)
            return

        # Start file upload ...
        total = sum(e.stats.st_size for e in uploads.values())
        ctx.print("{}Uploading {} files ({}) ...", dryrun, len(uploads), hbytes(total))

        println = ctx.print
        replace = args.force or args.update
        wrap = False

        # Prepare progress bar, if applicable
        if args.progress and not (ctx.print.quiet or dryrun):
            import tqdm

            pbar = tqdm.tqdm(
                total=total,
                unit="b",
                unit_scale=True,
                unit_divisor=1024,
                dynamic_ncols=True,
                file=ctx.print.file,
            )
            stack.enter_context(pbar)
            println = pbar.write

            def wrap(fp):
                for chunk in iter(lambda: fp.read(1024 * 64), b""):
                    pbar.update(len(chunk))
                    yield chunk

        for i, upload in enumerate(sorted(uploads.values())):
            prefix = "[{}/{}] ".format(i + 1, len(uploads))
            suffix = " (" + hbytes(upload.stats.st_size) + ")"
            println(dryrun + prefix + upload.remote + suffix)
            if dryrun:
                continue
            with open(upload.local, "rb") as fp:
                fp = wrap(fp) if wrap else fp
                client.put_file(vault, archive, upload.remote, fp, replace=replace)

        ctx.print(
            "\n{}Done! Uploaded {} files ({}) to archive: {}",
            dryrun,
            len(uploads),
            hbytes(total),
            archive,
        )

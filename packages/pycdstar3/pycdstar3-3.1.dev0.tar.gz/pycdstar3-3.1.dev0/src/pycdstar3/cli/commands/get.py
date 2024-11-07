"""
Download a single file from an archive.
"""

import os
import sys

from pycdstar3.cli import CliError
from pycdstar3.cli._utils import hbytes


def register(subparsers):
    parser = subparsers.add_parser(
        "get", help=__doc__.strip().splitlines()[0], description=__doc__
    )
    parser.add_argument(
        "-%",
        "-p",
        "--progress",
        action="store_true",
        help="Show progress bar for large files or slow downloads",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="If a <DST>.part file exists, try to resume an"
        " interrupted download. Also, keep the *.part file"
        " on any errors.",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Overwrite local files or print binary data to a terminal.",
    )
    parser.add_argument("ARCHIVE", help="Archive ID")
    parser.add_argument("FILE", help="File Name")
    parser.add_argument(
        "DST",
        nargs="?",
        help="Destination filename or directory."
        " No parameter or '-' prints to standard output. (default: '-')",
    )
    parser.set_defaults(main=get)


def get(ctx, args):  # noqa: C901
    client = ctx.client
    vault = ctx.vault
    archive = args.ARCHIVE
    file = args.FILE

    resume = args.resume
    progress = args.progress
    dst = args.DST or "-"
    force = args.force

    if not file:
        raise CliError("The <SRC> parameter must reference a file, not an archive")

    if dst.endswith("/") or os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(file))

    ispipe = dst == "-"
    partfile = dst + ".part" if not ispipe else None
    offset = 0

    if not ispipe and not force and os.path.exists(dst):
        raise CliError("File exists: " + dst)

    if partfile and os.path.exists(partfile):
        if resume:
            offset = os.path.getsize(partfile)
            ctx.print("Resuming download at: {}", hbytes(offset))
        else:
            raise CliError(
                "Found partial download, but --resume is not set: " + partfile
            )

    if ispipe:
        out = sys.stdout.buffer
    else:
        out = open(partfile, "ab")
    write = out.write
    close = out.close

    try:
        dl = client.get_file(vault, archive, file, offset=offset)

        if ispipe and out.isatty() and not dl.type.startswith("text/") and not force:
            raise CliError(
                "Not printing binary data ({}) to a terminal."
                " (--force not set)".format(dl.type)
            )

        if progress and not ctx.print.quiet:
            from tqdm import tqdm

            pbar = tqdm(
                total=dl.size + offset,
                initial=offset,
                unit="b",
                unit_scale=True,
                unit_divisor=1024,
                dynamic_ncols=True,
                file=ctx.print.file,
            )

            def write(chunk):
                pbar.update(len(chunk))
                out.write(chunk)

            def close():
                pbar.close()
                out.close()

        ctx.print.v("Downloading {} ({})", file, hbytes(dl.size + offset))

        for chunk in dl.iter_content():
            write(chunk)

        close()
        if not ispipe:
            if force:
                os.replace(partfile, dst)
            else:
                os.rename(partfile, dst)

        ctx.print.v("Done!", file, vault, archive, hbytes(dl.size + offset))

    except (KeyboardInterrupt, Exception):
        if close:
            close()
        if partfile and os.path.exists(partfile) and not resume:
            try:
                os.remove(partfile)
            except OSError:
                ctx.print("Failed to delete partial download: {}", partfile)
                raise
        raise

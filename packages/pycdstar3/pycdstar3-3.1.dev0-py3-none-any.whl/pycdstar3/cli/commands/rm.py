"""
Delete files from an archive.
"""

from contextlib import ExitStack
from pycdstar3 import ApiError

# TODO: Delete directories or glob patterns


def register(subparsers):
    parser = subparsers.add_parser(
        "rm", help=__doc__.strip().splitlines()[0], description=__doc__
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Ignore missing files or access errors",
    )

    parser.add_argument("ARCHIVE", help="Archive ID")
    parser.add_argument("FILES", nargs="+", help="File(s) to remove.")
    parser.set_defaults(main=remove_files)


def remove_files(ctx, args):
    client = ctx.client
    vault = ctx.vault
    archive = args.ARCHIVE

    files = args.FILES
    force = args.force

    with ExitStack() as stack:
        if len(files) > 1:
            stack.enter_context(client.begin(autocommit=True))

        for i, file in enumerate(files):
            file = file.lstrip("/")
            try:
                ctx.print("Deleting {}/{}".format(archive, file))
                client.delete_file(vault, archive, file)
            except ApiError as e:
                if e.error == "FileNotFound" and force:
                    continue
                raise

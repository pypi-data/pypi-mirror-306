"""
Remove one or more archives.
"""

from contextlib import ExitStack
from pycdstar3 import ApiError


def register(subparsers):
    parser = subparsers.add_parser(
        "rma", help=__doc__.strip().splitlines()[0], description=__doc__
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Do not prompt and ignore missing archives or access errors.",
    )
    parser.add_argument("-y", "--yes", action="store_true", help="Do not prompt")
    parser.add_argument(
        "ARCHIVE", nargs="+", help="Archive IDs. Repeat to delete multiple archives."
    )
    parser.set_defaults(main=remove_files)


def remove_files(ctx, args):
    client = ctx.client
    vault = ctx.vault
    archives = args.ARCHIVE
    force = args.force
    yes = args.yes

    with ExitStack() as stack:
        if len(archives) > 1:
            stack.enter_context(client.begin(autocommit=True))

        prompt = (
            "Do you really want to delete {} archives? "
            "This cannot be undone!".format(len(archives))
        )
        if not (yes or force or ctx.ask_yes(prompt)):
            return

        for archive in archives:
            try:
                client.delete_archive(vault, archive)
                ctx.print("Deleting: {}".format(archive))
            except ApiError as e:
                if force:
                    ctx.print("  Ignoring error (--force) {}", e)
                    continue
                raise

"""
Change storage profiles and wait form migrations to complete.
"""

import json

from pycdstar3 import FormUpdate
from pycdstar3.cli import CliError
from pycdstar3.cli._utils import KvArgType
from pycdstar3._utils import cascade_sleep


def register(subparsers):
    parser = subparsers.add_parser(
        "profile", help=__doc__.strip().splitlines()[0], description=__doc__
    )

    sub = parser.add_subparsers()

    pset = sub.add_parser("set", help="Set a new profile.")
    pset.add_argument("ARCHIVE", help="Archive ID")
    pset.add_argument("NAME", help="Profile name")
    pset.add_argument(
        "--wait", help="Wait for the migration to complete.", action="store_true"
    )
    pset.set_defaults(main=profile_set)

    pset = sub.add_parser("get", help="Print the current profile.")
    pset.add_argument("ARCHIVE", help="Archive ID")
    pset.add_argument(
        "--state", help="Also print the current migration state.", action="store_true"
    )

    pset.set_defaults(main=profile_get)

    pset = sub.add_parser("wait", help="Wait for migration to complete.")
    pset.add_argument("ARCHIVE", help="Archive ID")
    pset.set_defaults(main=profile_wait)


def profile_set(ctx, args):
    client = ctx.client

    update = FormUpdate()
    update.profile(args.NAME)
    client.update_archive(ctx.vault, args.ARCHIVE, form=update)

    if args.wait:
        _wait(ctx, ctx.vault, args.ARCHIVE)


def profile_get(ctx, args):
    info = ctx.client.archive_info(ctx.vault, args.ARCHIVE)
    if args.state:
        print(f"{info['profile']} {info['state']}")
    else:
        print(f"{info['profile']}")


def profile_wait(ctx, args):
    _wait(ctx, ctx.vault, args.ARCHIVE)


def _wait(ctx, vault, archive):
    if ctx.client.tx:
        raise CliError(
            "Migrations won't start until transaction is committed. Not waiting."
        )
    for total_wait in cascade_sleep(start=0.1, gain=0.1, maximum=10):
        info = ctx.client.archive_info(vault, archive)
        ctx.print(f"Archive state for [{info['id']}]: {info['state']}")
        if "pending-" not in info["state"]:
            break

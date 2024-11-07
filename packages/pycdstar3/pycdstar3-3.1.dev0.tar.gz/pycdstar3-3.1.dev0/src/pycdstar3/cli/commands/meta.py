"""
Show or modify archive or file meta attributes
"""

import json

from tabulate import tabulate

from pycdstar3 import FormUpdate
from pycdstar3.cli._utils import KvArgType


def register(subparsers):
    parser = subparsers.add_parser(
        "meta", help=__doc__.strip().splitlines()[0], description=__doc__
    )

    sub = parser.add_subparsers()

    pset = sub.add_parser("set")
    pset.add_argument("ARCHIVE", help="Archive ID")
    pset.add_argument(
        "--file",
        help="Set metadata of a file instead of the archive.",
    )
    pset.add_argument(
        "ATTR",
        metavar="NAME=VALUE",
        nargs="+",
        type=KvArgType("="),
        help="Set archive level permissions for a subject. ALLOW can be a "
        "comma-separated list of permission or permission-set names. Leave the "
        "ALLOW part empty to revoke all permissions for a subject.",
    )
    pset.set_defaults(main=meta_set)

    pshow = sub.add_parser("show")
    pshow.add_argument("ARCHIVE", help="Archive ID")
    pshow.add_argument(
        "--file",
        help="Get metadata from a file instead of the archive.",
    )

    pshow.add_argument(
        "-e",
        "--explode",
        action="store_true",
        help="Explode permission sets into individual permissions",
    )
    pshow.add_argument("--json", action="store_true", help="Print as JSON")
    pshow.set_defaults(main=meta_show)


def meta_set(ctx, args):
    client = ctx.client
    vault = ctx.vault
    archive = args.ARCHIVE
    file = args.file or None

    changes = {}
    for name, split, value in args.ATTR:
        # TODO: Support += and -= and @ to load from files
        if value:
            changes.setdefault(name, []).append(value)

    update = FormUpdate()
    for name, values in changes.items():
        update.meta(name, *values, file=file)
        ctx.print("Updating meta attribute {}: {}", name, values)

    client.update_archive(vault, archive, form=update)
    ctx.print("Done!")


def meta_show(ctx, args):
    client = ctx.client
    vault = ctx.vault
    archive = args.ARCHIVE
    file = args.file or None

    meta = client.meta_info(vault, archive, file)
    if args.json:
        print(json.dumps(meta, indent=4))
    elif meta:
        print(
            tabulate(
                sorted((k, v) for (k, vs) in meta.items() for v in vs),
                headers=["Name", "Value"],
            )
        )
    else:
        ctx.print("No meta attributes found")

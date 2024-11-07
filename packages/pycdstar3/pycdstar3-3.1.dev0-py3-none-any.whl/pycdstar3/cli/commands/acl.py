"""
Manage access control lists (ACL)
"""

import json

from tabulate import tabulate

from pycdstar3 import FormUpdate
from pycdstar3.cli._utils import KvArgType


def register(subparsers):
    parser = subparsers.add_parser(
        "acl", help=__doc__.strip().splitlines()[0], description=__doc__
    )
    sub = parser.add_subparsers()

    pset = sub.add_parser("set")
    pset.add_argument("ARCHIVE", help="Archive ID")
    pset.add_argument(
        "ALLOW",
        metavar="SUBJECT=ALLOW",
        nargs="+",
        type=KvArgType("="),
        help="Set archive level permissions for a subject. ALLOW can be a "
        "comma-separated list of permission or permission-set names. Leave the "
        "ALLOW part empty to revoke all permissions for a subject.",
    )
    pset.set_defaults(main=acl_set)

    pshow = sub.add_parser("show")
    pshow.add_argument("ARCHIVE", help="Archive ID")
    pshow.add_argument(
        "-e",
        "--explode",
        action="store_true",
        help="Explode permission sets into individual permissions",
    )
    pshow.add_argument("--json", action="store_true", help="Print as JSON")
    pshow.set_defaults(main=acl_show)


def acl_set(ctx, args):
    client = ctx.client
    vault = ctx.vault
    archive = args.ARCHIVE

    changes = {}
    for sub, split, allow in args.ALLOW:
        # TODO: Support += and -=
        if sub:
            changes.setdefault(sub, set()).update(filter(None, allow.split(",")))

    update = FormUpdate()
    for sub, allow in sorted(changes.items()):
        update.acl(sub, *allow)
        plist = ", ".join(sorted(allow)) if allow else ""
        ctx.print("{} => [{}]", sub, plist)

    client.update_archive(vault, archive, form=update)
    ctx.print("Done!")


def acl_show(ctx, args):
    client = ctx.client
    vault = ctx.vault
    archive = args.ARCHIVE

    acl = client.acl_info(vault, archive, explode=args.explode)
    if args.json:
        print(json.dumps(acl, indent=4))
    else:
        print(
            tabulate(
                sorted((k, ",".join(v)) for (k, v) in acl.items()),
                headers=["Subject", "Permissions"],
            )
        )

"""
Scroll all IDs in a vault.

By default, all IDs ever created in a vault are returned, including deleted or
private archives. This requires `list` vault permission on non-public vaults.

You can fall back on search-based scrolling if available, or enable `strict`
mode to only list archives load-able by the current user.
"""


def register(subparsers):
    parser = subparsers.add_parser(
        "scroll", help=__doc__.strip().splitlines()[0], description=__doc__
    )
    parser.add_argument(
        "--use-search",
        action="store_true",
        help="Retrieve IDs using search instead of the scroll api",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict-mode and only return IDs that are load-able by the current user",
    )
    parser.add_argument("START", nargs="?", help="Start with this ID.")

    parser.set_defaults(main=scroll)


def qescape(s):
    for c in '+-=&|><!(){}[]^"~*?:\\/':
        s = s.replace(c, "\\" + c)
    return s


def scroll(ctx, args):
    client = ctx.client
    vault = ctx.vault

    start = args.START or ""

    if args.use_search:
        q = "is:archive"
        if start:
            q = "{} AND id:>{}".format(q, qescape(start))
        for hit in client.iter_search(vault, q, order="id"):
            print(hit.id)
    else:
        for aid in client.iter_scroll(vault, start=start, strict=args.strict):
            print(aid)

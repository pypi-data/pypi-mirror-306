"""
Search a vault.

Query syntax and query-able index fields depend on the installed
search-backend and configuration. Search might be disabled or restricted
on your CDSTAR server instance. Please refer to your instance documentation
for details.

"""


def register(subparsers):
    parser = subparsers.add_parser(
        "search", help=__doc__.strip().splitlines()[0], description=__doc__
    )
    parser.add_argument(
        "--limit", type=int, default=25, help="Show this many results (default: 25)"
    )
    parser.add_argument(
        "--order",
        action="append",
        help="Order by index field name. Prefix with '-' to reverse"
        " ordering. Multiple (default: -score)",
    )
    parser.add_argument(
        "--no-scroll",
        action="store_true",
        help="Disables auto-fetching more results scrolling if less than --limit hits "
        "were returned.",
    )
    parser.add_argument(
        "QUERY", help="Search query. Syntax depends on back-end configuration."
    )

    parser.set_defaults(main=search)


def search(ctx, args):
    client = ctx.client
    vault = ctx.vault

    limit = max(1, args.limit)
    order = args.order or ["-score"]
    query = args.QUERY

    scroll = ""
    found = 0
    page = None
    while limit > found:
        page = client.search(
            vault, query, limit=min(1024, limit - found), order=order, scroll=scroll
        )

        if not page.hits:
            break  # no more results

        for hit in page.hits or []:
            found += 1

            if hit.type == "archive":
                print("{}".format(hit.id))
            elif hit.type == "file":
                print("{}\t{}".format(hit.id, hit.name))

            if found >= limit:
                break

        if args.no_scroll:
            break

        scroll = page.scroll

    ctx.print("Total results: {} ({} shown)".format(page.total, found))

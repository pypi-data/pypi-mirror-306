"""
List files in an archive or in a sub directory.

"""

from collections import defaultdict

import iso8601

from pycdstar3.cli import CliError
from pycdstar3.cli._utils import hbytes


def register(subparsers):
    parser = subparsers.add_parser(
        "ls", help=__doc__.strip().splitlines()[0], description=__doc__
    )
    parser.add_argument(
        "-f",
        "--format",
        default="name",
        help="Change what is printed per file. Provide either a python format string, "
        "or a csv with field names. Available fields: "
        "name, id, type, size, created, modified, md5, sha1, sha256, meta[...]\n"
        " (default: name)",
    )

    parser.add_argument(
        "--dates",
        choices=["local", "iso", "epoch"],
        default="local",
        help="Change the way dates are displayed",
    )

    parser.add_argument(
        "--order",
        default="name",
        choices=["name", "type", "size", "created", "modified", "hash", "id"],
        help="Order by name, type, size, created, modified, hash or id. "
        "(default: name)",
    )
    parser.add_argument("--reverse", action="store_true", help="Reverse list order")
    parser.add_argument(
        "-i",
        "--include",
        metavar="GLOB",
        action="append",
        help="Include files by glob pattern (default: all)",
    )
    parser.add_argument(
        "-x",
        "--exclude",
        metavar="GLOB",
        action="append",
        help="Exclude files by glob pattern",
    )
    parser.add_argument("ARCHIVE", help="Archive to list")
    parser.add_argument("PREFIX", nargs="?", help="Directory to list", default="/")

    parser.set_defaults(main=ls)


def ls(ctx, args):  # noqa: C901
    client = ctx.client
    vault = ctx.vault
    archive = args.ARCHIVE
    prefix = args.PREFIX

    opts = {"order": args.order, "reverse": args.reverse}
    if prefix.strip("/"):
        opts["include_glob"] = ["/{}/**".format(prefix.strip("/"))]
    if args.include:
        opts.setdefault("include_glob", []).append(args.include)
    if args.exclude:
        opts.setdefault("exclude_glob", []).append(args.exclude)

    fmt = (
        args.format.replace("\\t", "\t")
        .replace("\\0", "\0")
        .replace("\\n", "\n")
        .replace("\\\\", "\\")
    )

    if "{" not in fmt:
        # translate csv format to tab separated format string
        fmt = "{" + "}\t{".join(fmt.split(",")) + "}"

    if "{meta" in fmt:
        # Load metadata only if requested
        opts["meta"] = True

    def datefunc(date):
        dt = iso8601.parse_date(date)
        if args.dates == "epoch":
            return str(int(dt.timestamp()))
        if args.dates == "local":
            return dt.astimezone().replace(microsecond=0, tzinfo=None)
        if args.dates == "iso":
            return dt.astimezone().strftime("%Y-%m-%dT%H:%M:%S%z")
        raise CliError("Unknown date format: " + args.dates)

    with client.begin(readonly=True):
        n = b = 0
        for file in client.iter_files(vault, archive, **opts):
            n += 1
            b += file["size"]
            print(file2str(fmt, file, datefunc=datefunc))
        ctx.print()
        ctx.print("Total: {:,} files  {:,} bytes", n, b)


def file2str(fmt, file, datefunc):
    attrs = defaultdict(lambda: "-")
    attrs.update(file)
    attrs.update(file["digests"])

    if "{hsize" in fmt:
        attrs["hsize"] = hbytes(attrs["size"])
    if "{created" in fmt:
        attrs["created"] = datefunc(attrs["created"])
    if "{modified" in fmt:
        attrs["modified"] = datefunc(attrs["modified"])
    if "{meta" in fmt:
        meta = defaultdict(lambda: "-")
        meta.update(attrs["meta"])
        attrs["meta"] = meta
    return fmt.format_map(attrs)

"""
Initialize a cdstar working directory.

Create a config file in the current directory, so it can be found by future invocations
of cdstar-cli commands. Settings not provided as command line arguments are asked for
interactively.

If the main --config parameter is set, the configuration is saved at the specified
location instead of the current working directory.

"""

import os
import re

from pycdstar3.api import CDStar
from pycdstar3.cli import CliError
from pycdstar3.cli.context import Workspace


def register(subparsers):
    parser = subparsers.add_parser(
        "init", help=__doc__.strip().splitlines()[0], description=__doc__
    )
    parser.add_argument(
        "PATH",
        nargs="?",
        help="Folder to turn into a workspace directory (default: '.')",
        default=".",
    )
    parser.set_defaults(main=command)


def command(ctx, args):
    root = os.path.abspath(args.PATH)
    work = Workspace(root)

    if os.path.exists(work.configdir) or os.path.exists(work.configfile):
        raise CliError("Config directory '{}' already exists.".format(work.configdir))

    ctx.print("Creating workspace in: {}", work.root)
    ctx.print()

    server = ask("CDSTAR Server URI", args.server, r"^https?://.*/?$")
    if not server.endswith("/"):
        server += "/"
    if not server.endswith("v3/"):
        server += "v3/"

    try:
        ctx.print("  Connecting to {} ... ", server, end="")
        info = CDStar(server).service_info()
        ctx.print("OK ({})", info.version.cdstar)
        vaults = info.vaults or []
        ctx.print("  Available vaults: {}", ", ".join(sorted(vaults)))
    except Exception:
        raise CliError("Failed to connect")

    ctx.print()
    vault = ask(
        "Select a vault",
        args.vault or (info.vaults and info.vaults[0]),
        choice=vaults,
        rx=".+",
    )

    work.store_config(server=server, vault=vault)

    ctx.print()
    ctx.print.v("Config saved to: {}", work.configfile)
    ctx.print("Created workspace directory: {}", work.root)


def ask(q, default=None, rx=None, choice=None, password=False):
    try:
        import readline  # noqa: F401
    except ImportError:
        pass

    while True:
        prompt = "{} [{}]: ".format(q, default) if default else "{}: ".format(q)
        if password:
            import getpass

            val = getpass.getpass(prompt)
        else:
            val = input(prompt)
        if not val:
            if default:
                return default
            print("No input. Try again...")
            continue
        if rx and not re.match(rx, val):
            print("This does not look right. Try again...")
            continue
        if choice and val not in choice:
            print("Please select one of: {}", choice)
            continue

        return val

"""
CDSTAR command-line client
"""

import argparse
import importlib
import json
import sys

from pycdstar3 import __version__ as VERSION, ApiError

__ALL__ = ["main", "printer"]

parser = argparse.ArgumentParser(prog="pycdstar3")
parser.add_argument(
    "--server",
    metavar="URI",
    help="CDSTAR server URI. Defaults to CDSTAR_SERVER environment variable or"
    " workspace settings.",
)
parser.add_argument(
    "--vault",
    metavar="NAME",
    help="Vault to work with. Defaults to CDSTAR_VAULT environment variable or"
    " workspace settings.",
)
parser.add_argument("--version", action="store_true", help="Print version and exit.")
_grp = parser.add_mutually_exclusive_group()
_grp.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    help="Print more info. Repeat to increase verbosity.",
)
_grp.add_argument(
    "-q", "--quiet", action="store_true", help="Be quiet. Only print errors."
)
subparsers = parser.add_subparsers(
    title="available commands",
    description='Run "COMAMND -h" to get help for a specific command.',
    metavar="COMMAND",
)


def _autodiscover_commands():
    """Autodiscover and import all modules in the pycdstar3.cli.commands namespace.

    This also works for namespace packages. Another approach would be to
    auto-discover all top-level modules named `pycdstar3_*`.
    """
    import pkgutil
    import pycdstar3.cli.commands

    for _, name, ispkg in pkgutil.iter_modules(pycdstar3.cli.commands.__path__):
        if ispkg:
            continue
        ipath = pycdstar3.cli.commands.__name__ + "." + name
        yield name, importlib.import_module(ipath)


def main(*args):  # noqa: C901
    # Load and register all built-in commands
    for name, command in _autodiscover_commands():
        command.register(subparsers)

    # Parse command line arguments (may fail)
    opts = parser.parse_args(args)

    if opts.version:
        print("pycdstar3-" + VERSION)
        sys.exit(0)

    if not hasattr(opts, "main"):
        # No sub-command specified
        parser.print_help()
        return 1

    from pycdstar3.cli.context import CliContext

    ctx = CliContext(opts, workdir=".")

    try:
        return opts.main(ctx, opts) or 0
    except KeyboardInterrupt:
        ctx.print("Exiting...")
        return 0
    except CliError as e:
        ctx.print.error(str(e))
        return e.return_code
    except ApiError as e:
        ctx.print.error(str(e))
        ctx.print.v("Full error response:")
        ctx.print.v(json.dumps(e.json, indent=2), indent=2)
        return e.status
    except Exception as e:
        ctx.print.fatal("Uncaught exception ({}: {}). Exiting...", type(e).__name__, e)
        return 1


class CliError(Exception):
    """Exception that will cause a clean command-line shutdown without any stack trace.

    The message will still be printed."""

    def __init__(self, *args, status=1):
        super().__init__(*args)
        self.return_code = status

import configparser
import os
import sys
import typing

try:
    # Nicer input() behavior
    import readline  # noqa: F401
except ImportError:
    pass

from pycdstar3 import CDStar, __url__ as help_url
from pycdstar3._utils import cached_property, url_split_auth
from pycdstar3.cli import CliError
from pycdstar3.cli._utils import walk_up, Printer

CONFDIR_NAME = ".cdstar"
CONFIG_NAME = "workspace.conf"
CONFIG_SECTION = "pycdstar3"
ENV_PREFIX = "CDSTAR_"


class CliContext:
    """Provide context and tools to CLI commands.

    This class may provide anything that is used by more than one command.
    For example a ready to use CDSTAR client, workspace config settings, default
    vault or other global settings. Some properties may raise CliError ask for
    user input.
    """

    def __init__(self, args, workdir="."):
        self.args = args
        self.workdir = os.path.abspath(str(workdir))

    @cached_property
    def print(self) -> Printer:
        """An instance of :class:`pycdstar3.cli._utils.Printer` to print optional
        messages to the user. Messages are printed to stderr, so only use it for
        complementary information, not for the primary results.
        """
        printer = Printer(level=0, file=sys.stderr)

        if self.args.quiet:
            printer.set_verbosity(-1)
        else:
            printer.set_verbosity(self.args.verbose)

        return printer

    @cached_property
    def client(self) -> CDStar:
        server_url = self._require_setting("server")
        url, user, pwd = url_split_auth(server_url)
        if user:
            return CDStar(url, auth=(user, pwd or self._ask_pass(server_url)))
        return CDStar(url)

    @cached_property
    def vault(self):
        return self._require_setting("vault")

    @cached_property
    def workspace(self) -> "Workspace":
        # TODO: Allow to set a workspace via ENV
        ws = _find_workspace(self.workdir)
        if ws:
            self.print.vv("Found workspace directory: {}", ws.root)
        return ws

    def _get_setting(self, name) -> typing.Any:
        """Look for a setting in command-line arguments, environment variables or
        workspace configuration."""
        return (
            getattr(self.args, name, None)
            or os.environ.get(ENV_PREFIX + name.upper())
            or (self.workspace and self.workspace.config.get(name))
        )

    def _require_setting(self, name) -> typing.Any:
        result = self._get_setting(name)
        if result:
            return result
        raise CliError(
            "Missing --{} parameter.\n\n"
            " Alternatively, set the {} environment variable or create a "
            "workspace.".format(name, ENV_PREFIX + name.upper())
        )

    def _ask_pass(self, url):
        # Enter password for {url.scheme}://{url.netloc}/{url.path}
        raise RuntimeError("Asking for password not implemented yet")

    def ask_yes(self, prompt, default="yes") -> bool:
        """Ask user for confirmation (Y|n)"""

        def is_true(s):
            return s.lower() in ("y", "yes", "ok", "true")

        def is_false(s):
            return s.lower() in ("n", "no", "false")

        while True:
            if is_true(default):
                val = input("{} (Y|n): ".format(prompt)).strip() or default
            else:
                val = input("{} (y|N): ".format(prompt)).strip() or default

            if is_true(val):
                return True
            if is_false(val):
                return False
            self.print('Please answer "yes" or "no" (Ctrl+C to abort)')


def _find_workspace(start="."):
    for path in walk_up(os.path.abspath(start)):
        if os.path.isfile(os.path.join(path, CONFDIR_NAME, CONFIG_NAME)):
            return Workspace(path)


class Workspace:
    """Workspace directory with configuration and more.

    Currently a workspace directory is simply a folder which contains a
    `.cdstar/workspace.conf` file.
    """

    def __init__(self, root, config_dir=CONFDIR_NAME, config_file=CONFIG_NAME):
        self.root = os.path.abspath(str(root))
        self.configdir = os.path.abspath(os.path.join(self.root, config_dir))
        self.configfile = os.path.abspath(os.path.join(self.configdir, config_file))

    def validate(self):
        for path in (self.configdir, self.configfile):
            if not os.path.isdir(path):
                raise CliError("Not a valid workspace: {} not found".format(path))

    @cached_property
    def config(self):
        cfg = configparser.ConfigParser()
        cfg.read(self.configfile)
        if CONFIG_SECTION not in cfg:
            return {}
        return dict(cfg[CONFIG_SECTION])

    def __contains__(self, item):
        return item in self.config

    def get(self, item, default=None):
        return self.config.get(item, default)

    def __getitem__(self, item):
        return self.config[item]

    def store_config(self, **settings):
        cfg = configparser.ConfigParser()
        if os.path.exists(self.configfile):
            cfg.read(self.configfile)
        cfg[CONFIG_SECTION] = settings

        os.makedirs(self.configdir, mode=0o700, exist_ok=True)
        with open(self.configfile, "w") as fp:
            fp.write(
                "# This is a pycdstar3 workspace config file. See {}\n".format(help_url)
            )
            cfg.write(fp)

        self.__dict__.pop("config", None)

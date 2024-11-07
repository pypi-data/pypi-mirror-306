import argparse
import os
import re
import sys


def walk_up(start):
    """Yield the input and all its parent directories."""
    current_dir = os.path.abspath(start)
    while os.path.isdir(current_dir):
        yield current_dir
        parent = os.path.abspath(os.path.join(current_dir, os.pardir))
        if parent == current_dir:
            break
        current_dir = parent


def hbytes(n, units=None, div=1024.0):
    for unit in units or ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"):
        if abs(n) < div:
            return "{:.1f}{}".format(n, unit).replace(".0", "")
        n /= div
    raise AssertionError("Number out of range")


class KvArgType:
    """Argparse type that parses a KEY=VALUE parameter into a tuple.
    The value may be empty, but the '=' is required."""

    def __init__(self, split="="):
        self.split = list(split)
        self.split.sort(key=lambda x: (-len(x), x))

    def __call__(self, val):
        for split in self.split:
            k, s, v = val.partition(split)
            if s:
                return k, s, v
        raise argparse.ArgumentTypeError(
            "Expected KAY{}VALUE argument.".format(self.split[0])
        )


def globtype(str):
    """Argparse type that accepts glob file patterns"""
    return compile_glob(str)


def compile_glob(pattern):
    parts = re.split(r"(\*\*|\*|\?)", pattern)
    res = ["^" if pattern.startswith("/") else ".*"]

    for i, part in enumerate(parts):
        if i % 2 == 0:
            res.append(re.escape(part))
        elif part == "*":
            res.append(r"[^/]+")
        elif part == "**":
            res.append(r".+")
        elif part == "?":
            res.append(r"[^/]")
    return re.compile("".join(res) + "$")


class FileProgress:
    def __init__(self, fp, chunksize=1024 * 8, **baropts):
        from requests.utils import super_len

        self.opts = baropts
        self.fp = fp
        self.len = super_len(fp)
        self.chunksize = chunksize

    def __iter__(self):
        from tqdm import tqdm

        with tqdm(
            total=self.len,
            unit="b",
            unit_scale=True,
            unit_divisor=1024,
            dynamic_ncols=True,
            **self.opts
        ) as pbar:
            read = self.fp.read
            update = pbar.update
            while True:
                chunk = read(self.chunksize)
                if not chunk:
                    break
                update(len(chunk))
                yield chunk
            pbar.close()


class Printer:
    """Helper class to print to stderr based on verbosity levels."""

    __slots__ = ("verbosity", "quiet", "file")

    def __init__(self, level=0, file=sys.stderr):
        self.verbosity = level
        self.quiet = level <= -1
        self.file = file

    set_verbosity = __init__

    def _print(self, msg="", *args, **kwargs):
        hr = kwargs.pop("highlight", None)
        indent = kwargs.pop("indent", 0)
        if args:
            msg = msg.format(*args)
        if indent:
            msg = "".join(" " * indent + line for line in msg.splitlines(True))
        if hr:
            ncols = self._ncols()
            msg = (
                (hr * ncols)
                + "\n"
                + msg
                + ("" if msg.endswith("\n") else "\n")
                + (hr * ncols)
            )
        print(msg, file=self.file, **kwargs)

    def _ncols(self):
        import shutil

        return shutil.get_terminal_size((40, 20))[0]

    def __call__(self, msg="", *args, **kwargs):
        """Print only if -q (--quiet) was NOT passed as a command-line parameter"""
        if self.verbosity >= 0:
            self._print(msg, *args, **kwargs)

    def v(self, msg="", *args, **kwargs):
        """Print only if -v was passed as a command-line parameter"""
        if self.verbosity >= 1:
            self._print(msg, *args, **kwargs)

    def vv(self, msg="", *args, **kwargs):
        """Print only if -vv was passed as a command-line parameter"""
        if self.verbosity >= 2:
            self._print(msg, *args, **kwargs)

    def vvv(self, msg="", *args, **kwargs):
        """Print only if -vvv was passed as a command-line parameter"""
        if self.verbosity >= 3:
            self._print(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        """Print an error message (if not quiet) in a very visible way."""
        self._print("WARN: " + msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Print an error message (if not quiet) and optionally (-vv) a stacktrace."""
        self._print("ERROR: " + msg, *args, **kwargs)
        if self.verbosity >= 2:
            import traceback

            self._print(traceback.format_exc(), highlight="=")

    def fatal(self, msg, *args, **kwargs):
        """Print an error message (even if quiet) and optionally (-vv) a stacktrace."""
        self._print("FATAL: " + msg, *args, **kwargs)
        if self.verbosity >= 2:
            import traceback

            self._print(traceback.format_exc(), highlight="=")
        else:
            self("Stacktrace not shown. Add -vv to print a full stacktrace.")

import sys
import pycdstar3.cli


def main():  # pragma: no cover
    return pycdstar3.cli.main(*sys.argv[1:])


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main() or 0)

"""A module for CLI implementation."""

from __future__ import annotations

import shutil
import sys
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    Namespace,
    RawDescriptionHelpFormatter,
)

from pyjlyric.parse import Parsers, get_lyric_text

from . import __version__


class HelpFormatter(
    ArgumentDefaultsHelpFormatter,
    RawDescriptionHelpFormatter,
):
    """Custom formatter class."""


def parse_args() -> Namespace:
    """Parse given command line arguments.

    Returns
    -------
        Namespace: argparse.Namespace
    """
    usage = [
        "supported sites:",
        *[str(parser.__doc__) for parser in Parsers],
    ]

    parser = ArgumentParser(
        prog="jrc",
        description="get lyric data by URL.",
        formatter_class=(
            lambda prog: HelpFormatter(
                prog,
                width=shutil.get_terminal_size(fallback=(120, 50)).columns,
                max_help_position=40,
            )
        ),
        epilog="\n  - ".join(usage),
    )
    parser.add_argument(
        "url",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser.parse_args()


def main() -> int:
    """CLI main."""
    args = parse_args()
    url = str(args.url)
    r = get_lyric_text(url)

    if r is None:
        print(f"Error: Invalid link or unsupported site - <{url}>.", file=sys.stderr)  # noqa: T201
        return 1
    print(r)  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""A module for CLI implementation."""

from __future__ import annotations

import shutil
import sys
import textwrap
from argparse import (
    ArgumentDefaultsHelpFormatter,
    ArgumentParser,
    Namespace,
    RawDescriptionHelpFormatter,
)
from os import linesep

from . import Parsers, __version__, parse


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
    r = parse(url)

    if r is None:
        print(f"Error: Invalid link or unsupported site - <{url}>.", file=sys.stderr)  # noqa: T201
        return 1

    lyric_sections = [linesep.join(paragraph) + linesep for paragraph in r.lyric_sections]
    lyricist_names = [i.text for i in r.lyricists]
    composer_names = [i.text for i in r.composers]
    print(  # noqa: T201
        textwrap.dedent(
            f"""
            ===
            Title:\t\t{r.title}
            Artist:\t\t{r.artist.text}
            Lyric:\t\t{" / ".join(lyricist_names) or "(No data)"}
            Composer:\t{" / ".join(composer_names) or "(No data)"}
            ===
            """,
        ),
    )

    print(linesep.join(lyric_sections))  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())

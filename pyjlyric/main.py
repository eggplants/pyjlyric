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
    usage = textwrap.dedent(
        f"""
    supported sites:
        - {f'{linesep}- '.join([str(parser.__doc__) for parser in Parsers])}
    """,
    )

    parser = ArgumentParser(
        prog="jrc",
        description="Get Japanese Music Lyric with Site URL.",
        formatter_class=(
            lambda prog: HelpFormatter(
                prog,
                width=shutil.get_terminal_size(fallback=(120, 50)).columns,
                max_help_position=40,
            )
        ),
        epilog=usage,
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
    r = parse(str(args.url))

    if r is None:
        return 1

    lyric_sections = [linesep.join(paragraph)+linesep for paragraph in r.lyric]
    lyricist_names = [i.text for i in r.lyricist]
    composer_names = [i.text for i in r.composer]
    print(textwrap.dedent( # noqa: T201
        f"""
        ===
        Title:\t\t{r.title}
        Artist:\t\t{r.artist.text}
        Lyric:\t\t{" / ".join(lyricist_names)}
        Composer:\t{" / ".join(composer_names)}
        ===
        """,
    ))

    print(linesep.join(lyric_sections)) # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())

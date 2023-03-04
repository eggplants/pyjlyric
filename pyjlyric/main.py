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

from pyjlyric.model import WithUrlText

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

    title = r.title
    artist = r.artist.text if isinstance(r.artist, WithUrlText) else r.artist
    artist = [a.text if isinstance(a, WithUrlText) else a for a in artist] if isinstance(artist, list) else artist

    lyricist = r.lyricist.text if isinstance(r.lyricist, WithUrlText) else r.lyricist
    lyricist = (
        [ly.text if isinstance(ly, WithUrlText) else ly for ly in lyricist] if isinstance(lyricist, list) else lyricist
    )

    composer = r.composer.text if isinstance(r.composer, WithUrlText) else r.composer
    composer = (
        [c.text if isinstance(c, WithUrlText) else c for c in composer] if isinstance(composer, list) else composer
    )

    print(  # noqa: T201
        textwrap.dedent(
            f"""\
            ===
            Title:\t\t{title}
            Artist:\t\t{artist or "(No data)"}
            Lyric:\t\t{lyricist or "(No data)"}
            Composer:\t{composer or "(No data)"}
            ===
            """,
        ).strip(),
    )

    lyric_sections = [linesep.join(paragraph) for paragraph in r.lyric_sections]
    print((linesep + linesep).join(lyric_sections).strip())  # noqa: T201
    return 0


if __name__ == "__main__":
    sys.exit(main())

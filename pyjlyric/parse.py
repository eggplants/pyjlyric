from __future__ import annotations

import textwrap
from os import linesep
from typing import TYPE_CHECKING

from pyjlyric.model import WithUrlText

from .animap.parser import AnimapLyricPageParser
from .evesta.parser import EvestaLyricPageParser
from .gakki.parser import GakkiLyricPageParser
from .hoick.parser import HoickLyricPageParser
from .jlyric.parser import JlyricLyricPageParser
from .joysound.parser import JoysoundLyricPageParser
from .jtotal.parser import JtotalLyricPageParser
from .kashinavi.parser import KashinaviLyricPageParser
from .musicbook.parser import MusicbookLyricPageParser
from .petitlyrics.parser import PetitlyricsLyricPageParser
from .utamap.parser import UtamapLyricPageParser
from .utanet.parser import UtanetLyricPageParser
from .utaten.parser import UtatenLyricPageParser

if TYPE_CHECKING:
    from pyjlyric.model import LyricPage

    from .base import BaseLyricPageParser


Parsers: tuple[type[BaseLyricPageParser], ...] = (
    AnimapLyricPageParser,
    EvestaLyricPageParser,
    GakkiLyricPageParser,
    HoickLyricPageParser,
    KashinaviLyricPageParser,
    JoysoundLyricPageParser,
    JlyricLyricPageParser,
    JtotalLyricPageParser,
    MusicbookLyricPageParser,
    PetitlyricsLyricPageParser,
    UtamapLyricPageParser,
    UtanetLyricPageParser,
    UtatenLyricPageParser,
)


def parse(url: str) -> LyricPage | None:
    for parser in Parsers:
        if parser.is_valid_url(url):
            return parser.parse(url)
    return None


def get_lyric_text(url: str) -> str | None:
    """CLI main."""
    r = parse(url)

    if r is None:
        return None

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

    lyric_sections = [linesep.join(paragraph) for paragraph in r.lyric_sections]

    return (
        textwrap.dedent(
            f"""\
            ===
            Title:\t\t{title}
            Artist:\t\t{artist or "(No data)"}
            Lyric:\t\t{lyricist or "(No data)"}
            Composer:\t{composer or "(No data)"}
            ===
            """,
        )
        + (linesep * 2).join(lyric_sections).strip()
    )

from __future__ import annotations

from typing import TYPE_CHECKING

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


__version__ = "0.0.1"

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


__all__ = (
    "__version__",
    "Parsers",
    "AnimapLyricPageParser",
    "EvestaLyricPageParser",
    "GakkiLyricPageParser",
    "HoickLyricPageParser",
    "JlyricLyricPageParser",
    "JoysoundLyricPageParser",
    "JtotalLyricPageParser",
    "KashinaviLyricPageParser",
    "MusicbookLyricPageParser",
    "PetitlyricsLyricPageParser",
    "UtamapLyricPageParser",
    "UtanetLyricPageParser",
    "UtatenLyricPageParser",
    "parse",
)

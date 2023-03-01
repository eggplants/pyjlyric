from __future__ import annotations

from typing import TYPE_CHECKING

from .jlyric.parser import JlyricLyricPageParser
from .kashinavi.parser import KashinaviLyricPageParser
from .utanet.parser import UtanetLyricPageParser
from .utaten.parser import UtatenLyricPageParser

if TYPE_CHECKING:
    from pyjlyric.models import LyricPage

    from .base import BaseLyricPageParser


__version__ = "0.0.0"

Parsers: tuple[type[BaseLyricPageParser], ...] = (
    KashinaviLyricPageParser,
    JlyricLyricPageParser,
    UtanetLyricPageParser,
    UtatenLyricPageParser,
)


def parse(url: str) -> LyricPage | None:
    for parser in Parsers:
        if parser.is_valid_url(url):
            return parser.parse(url)
    return None

"""<https://kashinavi.com>"""

import re

from bs4 import BeautifulSoup, NavigableString, Tag

from ..base import BaseLyricPageParser, BaseLyricPageParserError
from ..models import LyricPage, WithUrlText
from ..utils import get_captured_value, get_source, parse_obj_as_url
from .models import JSONLD

_KASHINAVI_PATTERN = r"^https://kashinavi\.com/song_view\.html\?(?P<pageid>\d+)"


class KashinaviLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class KashinaviLyricPageParser(BaseLyricPageParser):
    """https://kashinavi.com/song_view.html?<pageid>"""

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_KASHINAVI_PATTERN)
        m = re.match(pattern, url)
        return get_captured_value(m, "pageid") is not None

    @staticmethod
    def parse(url: str) -> LyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_KASHINAVI_PATTERN)
        m = re.match(pattern, url)
        val = get_captured_value(m, "pageid")
        if val is None:
            raise KashinaviLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise KashinaviLyricPageParserError from ConnectionError

        jsonld_tag: Tag = bs.find_all("script", type="application/ld+json")[1]

        jsonld_source = jsonld_tag.text
        jsonld = JSONLD.parse_raw(jsonld_source)

        artist = jsonld.recorded_as.by_artist

        return LyricPage(
            title=jsonld.name,
            page_url=parse_obj_as_url(url),
            pageid=val,
            artist=WithUrlText(link=artist.url, text=artist.name),
            composers=[WithUrlText(text=jsonld.composer.name, link=None)],
            lyricists=[WithUrlText(text=jsonld.lyricist.name, link=None)],
            arrangers=None,
            lyric_sections=[
                [i.text for i in section.children if isinstance(i, NavigableString)]
                for section in BeautifulSoup(jsonld.lyrics.text, "lxml").find_all("p")
            ],
        )

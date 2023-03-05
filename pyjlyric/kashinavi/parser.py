"""<https://kashinavi.com>"""

import re

from bs4 import BeautifulSoup, NavigableString, Tag

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.model import WithUrlText
from pyjlyric.util import get_captured_value, get_source, parse_obj_as_url

from .model import JSONLD, KashinaviLyricPage

_KASHINAVI_PATTERN = r"^https://kashinavi\.com/song_view\.html\?(?P<pageid>\d+)"


class KashinaviLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class KashinaviLyricPageParser(BaseLyricPageParser):
    """https://kashinavi.com/song_view.html?<pageid>"""

    _test = "https://kashinavi.com/song_view.html?155779"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_KASHINAVI_PATTERN)
        m = re.match(pattern, url)
        return get_captured_value(m, "pageid") is not None

    @staticmethod
    def parse(url: str) -> KashinaviLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_KASHINAVI_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise KashinaviLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise KashinaviLyricPageParserError from ConnectionError

        jsonld_tag: Tag = bs.find_all("script", type="application/ld+json")[1]

        jsonld_source = jsonld_tag.text
        jsonld = JSONLD.parse_raw(jsonld_source)

        artist = jsonld.recorded_as.by_artist

        return KashinaviLyricPage(
            title=jsonld.name,
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(link=artist.url, text=artist.name),
            composer=jsonld.composer.name,
            lyricist=jsonld.lyricist.name,
            arranger=None,
            lyric_sections=[
                [i.text for i in section.children if isinstance(i, NavigableString)]
                for section in BeautifulSoup(jsonld.lyrics.text, "lxml").find_all("p")
            ],
        )

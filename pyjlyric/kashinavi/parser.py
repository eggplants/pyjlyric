"""<https://kashinavi.com>"""

import re

from bs4 import NavigableString

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.model import WithUrlText
from pyjlyric.util import get_captured_value, get_source, parse_obj_as_url, select_one_tag

from .model import KashinaviLyricPage

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

        artist_link = select_one_tag(bs, "body > center > p > a:nth-child(2)").get("href")
        if not isinstance(artist_link, str):
            raise KashinaviLyricPageParserError from ValueError

        if not (m := re.match(r"^「(.+)」歌詞$", select_one_tag(bs, "h2").text)):
            raise KashinaviLyricPageParserError from ValueError
        title = m.group(1)

        detail_tag = select_one_tag(bs, "tr > td[align=right] > div:nth-child(1)")
        if not (m := re.match(r"^歌手：(.+)作詞：(.+)作曲：(.+)$", detail_tag.text)):  # noqa: RUF001
            raise KashinaviLyricPageParserError from ValueError
        artist, lyricist, composer = m.groups()

        return KashinaviLyricPage(
            title=title,
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(link=parse_obj_as_url(artist_link), text=artist),
            composer=composer,
            lyricist=lyricist,
            arranger=None,
            lyric_sections=[
                [i.text for i in section.children if isinstance(i, NavigableString)]
                for section in select_one_tag(bs, "div[unselectable='on;']").find_all("p")
            ],
        )

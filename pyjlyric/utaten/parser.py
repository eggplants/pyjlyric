"""<https://utaten.com>"""

import re

from bs4 import Tag

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.util import (
    get_captured_value,
    get_source,
    parse_obj_as_url,
    parse_text_with_optional_link,
    select_one_tag,
)

from .model import UtatenLyricPage

_UTATEN_PATTERN = r"^https://utaten\.com/lyric/(?P<pageid>[a-z]{2}\d+)/?$"


class UtatenLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class UtatenLyricPageParser(BaseLyricPageParser):
    """https://utaten.com/lyric/<pageid>"""

    _test = "https://utaten.com/lyric/ma21111253/"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_UTATEN_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> UtatenLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_UTATEN_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise UtatenLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise UtatenLyricPageParserError from ConnectionError

        title_h2 = select_one_tag(bs, "h2.newLyricTitle__main")
        for span in title_h2.select("span.newLyricTitle_afterTxt"):
            span.replace_with("")

        artist = select_one_tag(bs, "dt.newLyricWork__name > h3 > a")
        artist_link = (
            None
            if artist.href is None
            else parse_obj_as_url(
                artist.href.text,
                base=url,
            )
        )

        composer_dt = bs.find("dt", string="作曲")
        if not isinstance(composer_dt, Tag):
            raise UtatenLyricPageParserError from TypeError

        composer_dd = composer_dt.findNext("dd")
        if not isinstance(composer_dd, Tag):
            raise UtatenLyricPageParserError from TypeError

        composer_link = (
            None
            if composer_dd.href is None
            else parse_obj_as_url(
                composer_dd.href.text,
                base=url,
            )
        )

        lyricist_dt = bs.find("dt", string="作詞")
        if not isinstance(lyricist_dt, Tag):
            raise UtatenLyricPageParserError from TypeError

        lyricist_dd = lyricist_dt.findNext("dd")
        if not isinstance(lyricist_dd, Tag):
            raise UtatenLyricPageParserError from TypeError

        lyricist_link = (
            None
            if lyricist_dd.href is None
            else parse_obj_as_url(
                lyricist_dd.href.text,
                base=url,
            )
        )

        arranger_dt = bs.find("dt", string="編曲")
        if not isinstance(arranger_dt, Tag):
            arranger_dt = None

        arranger_dd = None if arranger_dt is None else lyricist_dt.findNext("dd")
        if not isinstance(arranger_dd, Tag):
            arranger_dd = None

        arranger_link = (
            None
            if arranger_dd is None or arranger_dd.href is None
            else parse_obj_as_url(
                arranger_dd.href.text,
                base=url,
            )
        )

        lyric = select_one_tag(bs, "div.lyricBody > div > div.hiragana")
        for span in lyric.select("span.rt"):
            span.replace_with("")

        return UtatenLyricPage(
            title=title_h2.text.strip(),
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=parse_text_with_optional_link(artist.text.strip(), artist_link),
            composer=parse_text_with_optional_link(composer_dd.text.strip(), composer_link),
            lyricist=parse_text_with_optional_link(lyricist_dd.text.strip(), lyricist_link),
            arranger=None if arranger_dd is None else parse_text_with_optional_link(arranger_dd.text, arranger_link),
            lyric_sections=[section.strip().split("\n") for section in lyric.text.replace("\u3000", " ").split("\n\n")],
        )

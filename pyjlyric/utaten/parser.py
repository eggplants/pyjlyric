"""<https://kashinavi.com>"""

import re
from urllib.parse import urljoin

from bs4 import Tag

from ..base import BaseLyricPageParser, BaseLyricPageParserError
from ..models import LyricPage, WithUrlText
from ..utils import get_captured_value, get_source, parse_obj_as_url, select_one_tag

_UTATEN_PATTERN = r"^https://utaten.com/lyric/(?P<pageid>[a-z]{2}\d+)/$"


class UtatenLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class UtatenLyricPageParser(BaseLyricPageParser):
    """https://www.uta-net.com/song/<pageid>/"""

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_UTATEN_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> LyricPage:
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
                urljoin(url, artist.href.text),
            )
        )

        composer_dt = bs.find("dt", text="作曲")
        if not isinstance(composer_dt, Tag):
            raise UtatenLyricPageParserError from TypeError

        composer_dd = composer_dt.findNext("dd")
        if not isinstance(composer_dd, Tag):
            raise UtatenLyricPageParserError from TypeError

        composer_link = (
            None
            if composer_dd.href is None
            else parse_obj_as_url(
                urljoin(url, composer_dd.href.text),
            )
        )

        lyricist_dt = bs.find("dt", text="作詞")
        if not isinstance(lyricist_dt, Tag):
            raise UtatenLyricPageParserError from TypeError

        lyricist_dd = lyricist_dt.findNext("dd")
        if not isinstance(lyricist_dd, Tag):
            raise UtatenLyricPageParserError from TypeError

        lyricist_link = (
            None
            if lyricist_dd.href is None
            else parse_obj_as_url(
                urljoin(url, lyricist_dd.href.text),
            )
        )

        arranger_dt = bs.find("dt", text="編曲")
        if not isinstance(arranger_dt, Tag):
            arranger_dt = None

        arranger_dd = None if arranger_dt is None else lyricist_dt.findNext("dd")
        if not isinstance(arranger_dd, Tag):
            arranger_dd = None

        arranger_link = (
            None
            if arranger_dd is None or arranger_dd.href is None
            else parse_obj_as_url(
                urljoin(url, arranger_dd.href.text),
            )
        )

        lyric = select_one_tag(bs, "div.lyricBody > div > div.hiragana")
        for span in lyric.select("span.rt"):
            span.replace_with("")

        return LyricPage(
            title=title_h2.text.strip(),
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(text=artist.text.strip(), link=artist_link),
            composers=[WithUrlText(text=composer_dd.text.strip(), link=composer_link)],
            lyricists=[WithUrlText(text=lyricist_dd.text.strip(), link=lyricist_link)],
            arrangers=arranger_dd
            if arranger_dd is None
            else [
                WithUrlText(text=arranger_dd.text, link=arranger_link),
            ],
            lyric_sections=[section.strip().split("\n") for section in lyric.text.replace("\u3000", " ").split("\n\n")],
        )

"""<https://lyric.evesta.com>"""

import re

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.model import WithUrlText
from pyjlyric.util import get_captured_value, get_source, parse_obj_as_url, select_one_tag

from .model import HoickLyricData, HoickLyricPage

_HOICK_PATTERN = r"^https://hoick\.jp/mdb/detail/(?P<pageid>\d+)/?.*$"


class HoickLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class HoickLyricPageParser(BaseLyricPageParser):
    """https://hoick.jp/mdb/detail/<pageid>"""

    _test = "https://hoick.jp/mdb/detail/5144/%e3%82%b1%e3%83%ad%e3%83%9d%e3%83%b3%e4%bd%93%e6%93%8d"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_HOICK_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> HoickLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_HOICK_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise HoickLyricPageParserError from ValueError

        bs = get_source(url, parser="html.parser")
        if bs is None:
            raise HoickLyricPageParserError from ConnectionError

        header_div = select_one_tag(bs, "div.m_bottom")

        lyricists = [
            WithUrlText(text=a.text, link=parse_obj_as_url(a.href.text, base=url))
            for a in select_one_tag(header_div, "h2.lylic").select("a")
            if a.href is not None
        ]

        composers = [
            WithUrlText(text=a.text, link=parse_obj_as_url(a.href.text, base=url))
            for a in select_one_tag(header_div, "h2.music").select("a")
            if a.href is not None
        ]

        bs_lyric = get_source(f"https://hoick.jp/data.php?id={pageid}&type=4")
        if bs_lyric is None:
            raise HoickLyricPageParserError from ConnectionError
        lyric_lines = HoickLyricData.model_validate_json(bs_lyric.text)

        return HoickLyricPage(
            title=select_one_tag(bs, "h1.detail").text,
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=None,
            composer=composers,
            lyricist=lyricists,
            arranger=None,
            lyric_sections=[section.strip().split("\r") for section in "".join(lyric_lines.root[:-1]).split("\r\r")],
        )

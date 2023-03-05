"""<http://www.animap.jp>"""

import re

import requests
from bs4 import BeautifulSoup

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.util import get_captured_value, parse_obj_as_url, select_one_tag

from .model import AnimapLyricPage

_ANIMAP_PATTERN = r"^http://www\.animap\.jp/kasi/showkasi\.php\?surl=(?P<pageid>(?:ani|k-)\d+(?:-\d+)*)$"


class AnimapLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class AnimapLyricPageParser(BaseLyricPageParser):
    """http://www.animap.jp/kasi/showkasi.php?surl=<pageid>"""

    _test = "http://www.animap.jp/kasi/showkasi.php?surl=k-180131-061"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_ANIMAP_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> AnimapLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_ANIMAP_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise AnimapLyricPageParserError from ValueError

        bs = BeautifulSoup(requests.get(url, timeout=10).text.encode("shift_jis", "ignore"), "lxml")
        if bs is None:
            raise AnimapLyricPageParserError from ConnectionError

        lyric = select_one_tag(bs, "td.noprint.kasi_honbun")
        for br in lyric.select("br"):
            br.replace_with("\n")

        return AnimapLyricPage(
            title=select_one_tag(bs, "tr:nth-child(2) > td:nth-child(2)").text.strip(),
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=select_one_tag(bs, "tr:nth-child(1) > td:nth-child(2)").text.strip(),
            composer=select_one_tag(bs, "tr:nth-child(2) > td:nth-child(4)").text.strip(),
            lyricist=select_one_tag(bs, "tr:nth-child(1) > td:nth-child(4)").text.strip(),
            arranger=None,
            lyric_sections=[section.strip().split("\n") for section in lyric.text.strip().split("\n\n")],
        )

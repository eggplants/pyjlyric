"""<http://www.animap.jp>"""

import re

from ..base import BaseLyricPageParser, BaseLyricPageParserError
from ..models import LyricPage, WithUrlText
from ..utils import get_captured_value, get_source, parse_obj_as_url, select_one_tag

_ANIMAP_PATTERN = r"^http://www\.animap\.jp/kasi/showkasi\.php\?surl=(?P<pageid>(?:ani|k-)\d+(?:-\d+)*)$"


class AnimapLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class AnimapLyricPageParser(BaseLyricPageParser):
    """http://www.animap.jp/kasi/showkasi.php?surl=<pageid>"""

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_ANIMAP_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> LyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_ANIMAP_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise AnimapLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise AnimapLyricPageParserError from ConnectionError

        lyric = select_one_tag(bs, "td.noprint.kasi_honbun")
        for br in lyric.select("br"):
            br.replace_with("\n")

        return LyricPage(
            title=select_one_tag(bs, "tr:nth-child(2) > td:nth-child(2)").text.strip(),
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(text=select_one_tag(bs, "tr:nth-child(1) > td:nth-child(2)").text.strip(), link=None),
            composers=[WithUrlText(text=select_one_tag(bs, "tr:nth-child(2) > td:nth-child(4)").text, link=None)],
            lyricists=[
                WithUrlText(text=select_one_tag(bs, "tr:nth-child(1) > td:nth-child(4)").text.strip(), link=None),
            ],
            arrangers=None,
            lyric_sections=[section.strip().split("\n") for section in lyric.text.strip().split("\n\n")],
        )

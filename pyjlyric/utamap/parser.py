"""<http://www.animap.jp>"""

import re

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.jlyric.model import JlyricLyricPage
from pyjlyric.util import get_captured_value, get_source, parse_obj_as_url, select_one_tag

_UTAMAP_PATTERN = r"^https://www\.utamap\.com/showtop\.php\?surl=(?P<pageid>\d+)$"


class UtamapLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class UtamapLyricPageParser(BaseLyricPageParser):
    """http://www.utamap.com/showtop.php?surl=<pageid>"""

    _test = "https://www.utamap.com/showtop.php?surl=58401"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_UTAMAP_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> JlyricLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_UTAMAP_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise UtamapLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise UtamapLyricPageParserError from ConnectionError

        lyric = select_one_tag(bs, "td.noprint.kasi_honbun")
        for br in lyric.select("br"):
            br.replace_with("\n")

        return JlyricLyricPage(
            title=select_one_tag(bs, "td.kasi1").text,
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=select_one_tag(bs, "tr:nth-child(3) > td:nth-child(2).pad5x10x0x10 > strong").text.strip(),
            composer=select_one_tag(bs, "tr:nth-child(2) > td:nth-child(2).pad5x10x0x10").text.strip(),
            lyricist=select_one_tag(bs, "tr:nth-child(1) > td:nth-child(2).pad5x10x0x10").text.strip(),
            arranger=None,
            lyric_sections=[section.strip().split("\n") for section in lyric.text.strip().split("\n\n")],
        )

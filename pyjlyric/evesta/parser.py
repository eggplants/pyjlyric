"""<https://lyric.evesta.com>"""

import re
from urllib.parse import urljoin

from ..base import BaseLyricPageParser, BaseLyricPageParserError
from ..models import LyricPage, WithUrlText
from ..utils import get_captured_value, get_source, parse_obj_as_url, select_one_tag

_EVESTA_PATTERN = r"^https://lyric.evesta.jp/(?P<pageid>l\d+)\.html$"


class EvestaLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class EvestaLyricPageParser(BaseLyricPageParser):
    """https://lyric.evesta.jp/<pageid>.html"""

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_EVESTA_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> LyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_EVESTA_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise EvestaLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise EvestaLyricPageParserError from ConnectionError

        header_div = select_one_tag(bs, "div#lyrictitle")

        artist = select_one_tag(header_div, "#lyrictitle > p:nth-child(2) > a")
        artist_link = (
            None
            if artist is None or artist.href is None
            else parse_obj_as_url(
                urljoin(url, artist.href.text),
            )
        )

        lyricist = select_one_tag(header_div, "#lyrictitle > p:nth-child(3)")

        composer = select_one_tag(header_div, "#lyrictitle > p:nth-child(4)")

        lyric = select_one_tag(bs, "div#lyricbody")
        for br in lyric.select("br"):
            br.replace_with("")

        return LyricPage(
            title=re.sub(r"\s歌詞$", "", select_one_tag(header_div, "h1").text),
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(text=artist.text, link=artist_link),
            composers=[WithUrlText(text=composer.text, link=None)],
            lyricists=[WithUrlText(text=lyricist.text, link=None)],
            arrangers=None,
            lyric_sections=[section.strip().split("\r\n") for section in lyric.text.strip().split("\n\r\n")],
        )

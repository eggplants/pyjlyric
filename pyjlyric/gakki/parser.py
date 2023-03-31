"""<https://lyric.evesta.com>"""

import re

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.model import WithUrlText
from pyjlyric.util import convert_lines_into_sections, get_captured_value, get_source, parse_obj_as_url, select_one_tag

from .model import GakkiLyricPage

_GAKKI_PATTERN = r"^https://gakufu.gakki.me/m/data/(?P<pageid>[A-Z]+\d+)\.html$"


class GakkiLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class GakkiLyricPageParser(BaseLyricPageParser):
    """https://gakufu.gakki.me/m/data/<pageid>.html"""

    _test = "https://gakufu.gakki.me/m/data/RQ17577.html"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_GAKKI_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> GakkiLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_GAKKI_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise GakkiLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise GakkiLyricPageParserError from ConnectionError
        m = re.match(r"^作詞\s(?P<lyricist>.*)\s作曲\s(?P<composer>.*)$", select_one_tag(bs, "div.info > p.data").text)
        if m is None:
            raise GakkiLyricPageParserError from ValueError

        lyricist, composer = str(m.group("lyricist")), str(m.group("composer"))

        artist = select_one_tag(bs, "#topics > ol > li:nth-child(2) > a")

        lyric_chars = []
        for div in bs.select("div#chord_area > div"):
            if div.get("class") is None:
                lyric_chars.append("\n")
            else:
                lyric_chars.extend(d.text for d in div.select("div.cd_pic.blue > div") if not d.text.strip())

        lyric_lines = [i.replace("\n", "") for i in "\n".join(lyric_chars).strip().split("\n\n\n")]

        return GakkiLyricPage(
            title=select_one_tag(bs, "div.info > h2.tit > span").text[1:-1],
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(text=artist.text.strip(), link=parse_obj_as_url(str(artist.get("href")), base=url)),
            composer=composer,
            lyricist=lyricist,
            arranger=None,
            lyric_sections=convert_lines_into_sections(lyric_lines),
        )

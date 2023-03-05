"""<http://www.animap.jp>"""

import re

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.model import WithUrlText
from pyjlyric.util import get_captured_value, get_source, parse_obj_as_url, select_one_tag

from .model import JtotalLyricPage

_JTOTAL_PATTERN = r"^https://music\.j-total\.net/data/(?P<pageid>\d{3}[a-z]+/\d{3}[a-zA-Z_]+/\d{3})\.html$"


class JtotalLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class JtotalLyricPageParser(BaseLyricPageParser):
    """http://www.animap.jp/kasi/showkasi.php?surl=<pageid>"""

    _test = "https://music.j-total.net/data/004e/006_Elephant_Kashimashi/095.html"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_JTOTAL_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> JtotalLyricPage:
        """Parse the url page and return the result as LyricPage instance."""

        def is_valid_lyric(line: str) -> bool:
            line = line.strip()
            return line not in ("", "/") and not re.match("on.#", line) and not re.match("/.*/", line)

        pattern = re.compile(_JTOTAL_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise JtotalLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise JtotalLyricPageParserError from ConnectionError
        artist, lyricist, composer = select_one_tag(bs, "div.box2 > h2").text.split("/")
        artist_link = select_one_tag(bs, "body > div.wrapper > div.main > a").get("href")
        if artist_link is None:
            raise JtotalLyricPageParserError from ValueError

        lyric = select_one_tag(bs, "body > div.wrapper > div.main > p > tt")
        for a in lyric.select("a"):
            a.replace_with("")
        lyric_sections = [line.strip().split("\n") for line in lyric.text.split("\n\n")]
        lyric_sections = [
            [line.replace("\u3000", " ") for ly in lyric_section if is_valid_lyric(line := ly.strip())]
            for lyric_section in lyric_sections
        ]

        return JtotalLyricPage(
            title=select_one_tag(bs, "div.box2 > h1").text.strip(),
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(text=artist[2:], link=parse_obj_as_url(str(artist_link))),
            composer=composer,
            lyricist=lyricist,
            arranger=None,
            lyric_sections=[s for s in lyric_sections if len(s) > 0],
        )

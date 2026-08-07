"""<https://kashinavi.com>"""

from __future__ import annotations

import re

from bs4 import NavigableString, Tag

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.model import WithUrlText
from pyjlyric.util import get_captured_value, get_source, parse_obj_as_url, select_one_tag

from .model import KashinaviLyricPage

_KASHINAVI_PATTERN = r"^https://kashinavi\.com/lyrics/(?P<pageid>\d+)/?$"


class KashinaviLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class KashinaviLyricPageParser(BaseLyricPageParser):
    """https://kashinavi.com/lyrics/<pageid>/"""

    _test = "https://kashinavi.com/lyrics/155779/"

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

        overflow_div = select_one_tag(bs, "div[style*='overflow:hidden']")

        h2_span = select_one_tag(overflow_div, "h2 > span")
        title = re.sub(r"^「|」歌詞$", "", h2_span.text.strip()).strip()

        artist_a = select_one_tag(overflow_div, "a[href*='/artist/']")
        artist_link = artist_a.get("href")
        if not isinstance(artist_link, str):
            raise KashinaviLyricPageParserError from ValueError
        artist_text = artist_a.text.strip()

        detail_inner = select_one_tag(overflow_div, "div")
        lyricist = ""
        composer = ""
        for span in detail_inner.select("span"):
            text = span.text.strip()
            if text.startswith("作詞："):
                lyricist = text[3:].strip()
            elif text.startswith("作曲："):
                composer = text[3:].strip()

        if not lyricist or not composer:
            raise KashinaviLyricPageParserError from ValueError

        lyric_div = select_one_tag(bs, "div[style*='user-select:none']")
        lyric_sections: list[list[str]] = []
        current_lines: list[str] = []
        prev_was_br = False
        for child in lyric_div.children:
            if isinstance(child, Tag) and child.name == "br":
                if prev_was_br:
                    lyric_sections.append(current_lines)
                    current_lines = []
                    prev_was_br = False
                else:
                    prev_was_br = True
            elif isinstance(child, NavigableString) and (stripped := child.strip()):
                prev_was_br = False
                current_lines.append(stripped)
        if current_lines:
            lyric_sections.append(current_lines)

        return KashinaviLyricPage(
            title=title,
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(link=parse_obj_as_url(artist_link, base=url), text=artist_text),
            composer=composer,
            lyricist=lyricist,
            arranger=None,
            lyric_sections=lyric_sections,
        )

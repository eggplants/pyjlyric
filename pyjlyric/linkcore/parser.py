"""<https://linkco.re>"""

from __future__ import annotations

import re

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.util import (
    get_captured_value,
    get_source,
    parse_obj_as_url,
    parse_text_with_optional_link,
    select_one_tag,
)

from .model import LinkcoreLyricPage

_LINKCORE_PATTERN = r"^https://linkco\.re/(?P<albumid>[a-zA-Z0-9]+)/songs/(?P<songid>[0-9]+)/lyrics$"


class LinkcoreLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class LinkcoreLyricPageParser(BaseLyricPageParser):
    """https://linkco.re/<albumid>/songs/<songid>/lyrics"""

    _test = "https://linkco.re/0aQUYTE5/songs/1825986/lyrics"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_LINKCORE_PATTERN)
        m = re.match(pattern, url)
        albumid = get_captured_value(m, "albumid")
        songid = get_captured_value(m, "songid")

        return albumid is not None and songid is not None

    @staticmethod
    def parse(url: str) -> LinkcoreLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_LINKCORE_PATTERN)
        m = re.match(pattern, url)
        albumid = get_captured_value(m, "albumid")
        if albumid is None:
            raise LinkcoreLyricPageParserError from ValueError
        songid = get_captured_value(m, "songid")
        if songid is None:
            raise LinkcoreLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise LinkcoreLyricPageParserError from ConnectionError

        title_h2 = select_one_tag(bs, "div.header_text > h2")

        artist_h3 = select_one_tag(bs, "div.header_text > h3")
        artist_a = artist_h3.a
        artist_link = (
            None
            if artist_a is None or artist_a.href is None
            else parse_obj_as_url(
                artist_a.href.text,
                base=url,
            )
        )

        lyricist_p = select_one_tag(bs, "div.lyric_credit > ul > li:nth-child(1) > p")
        composer_p = select_one_tag(bs, "div.lyric_credit > ul > li:nth-child(2) > p")

        lyric_sections: list[list[str]] = [[]]
        for section in select_one_tag(bs, "div.lyric_text").find_all("p"):
            if section == "":
                lyric_sections.append([])
                continue
            lyric_sections[-1].append(section.text)

        return LinkcoreLyricPage(
            title=title_h2.text,
            page_url=parse_obj_as_url(url),
            pageid=f"{albumid}-{songid}",
            artist=(
                artist_h3.text.split(", ") if artist_h3 else parse_text_with_optional_link(artist_h3.text, artist_link)
            ),
            composer=composer_p.text.split(", "),
            lyricist=lyricist_p.text.split(", "),
            arranger=None,
            lyric_sections=lyric_sections,
        )

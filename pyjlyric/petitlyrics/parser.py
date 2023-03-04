"""<http://www.animap.jp>"""

import re

from pyjlyric.model import WithUrlText

from ..base import BaseLyricPageParser, BaseLyricPageParserError
from ..util import convert_lines_into_sections, get_captured_value, get_source, parse_obj_as_url, select_one_tag
from .model import PetitlyricsLyricData, PetitlyricsLyricPage

_PETITLYRICS_PATTERN = r"^https://petitlyrics\.com/lyrics/(?P<pageid>\d+)$"


class PetitlyricsLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class PetitlyricsLyricPageParser(BaseLyricPageParser):
    """https://petitlyrics.com/lyrics/<pageid>"""

    _test = "https://petitlyrics.com/lyrics/3287202"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_PETITLYRICS_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> PetitlyricsLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_PETITLYRICS_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise PetitlyricsLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise PetitlyricsLyricPageParserError from ConnectionError

        song_data_area = select_one_tag(bs, "td > div.pure-g > div.pure-u-1 > div:nth-child(1)")

        artist = select_one_tag(song_data_area, "p > a:nth-child(2)")
        artist_link = artist.get("href")
        if not isinstance(artist_link, str):
            raise PetitlyricsLyricPageParserError from ValueError

        m = re.search("(作詞\uff1a|Artist:)(?P<name>[^\u00a0]+)\u00a0", song_data_area.text)
        lyricist = None if m is None else get_captured_value(m, "name")

        m = re.search("(作曲\uff1a|Composer:)(?P<name>[^\u00a0]+)\u00a0", song_data_area.text)
        composer = None if m is None else get_captured_value(m, "name")

        bs_ajax = get_source(
            "https://petitlyrics.com/com/get_lyrics.ajax",
            data={
                "lyrics_id": pageid,
            },
            method="post",
            headers={
                "Cookie": "PLSESSION=vlfik4iua1vb2d898pv4vvqbjkcpblvt",
                "X-CSRF-Token": "3b1a3e3409715d8743233db0ad92bafa",
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        if bs_ajax is None:
            raise PetitlyricsLyricPageParserError from ConnectionError

        lyric_lines = list(PetitlyricsLyricData.parse_raw(bs_ajax.text))

        return PetitlyricsLyricPage(
            title=select_one_tag(bs, "div.title-bar").text.strip(),
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(text=artist.text.strip(), link=parse_obj_as_url(str(artist_link), base=url)),
            composer=None if composer is None else composer.strip(),
            lyricist=None if lyricist is None else lyricist.strip(),
            arranger=None,
            lyric_sections=convert_lines_into_sections(lyric_lines),
        )

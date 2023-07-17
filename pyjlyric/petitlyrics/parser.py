"""<http://www.animap.jp>"""

import re

from bs4 import BeautifulSoup
from requests import session

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.model import WithUrlText
from pyjlyric.util import convert_lines_into_sections, get_captured_value, parse_obj_as_url, select_one_tag

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

        sess = session()
        res = sess.get(url)
        if not res.ok:
            raise PetitlyricsLyricPageParserError from ConnectionError
        bs = BeautifulSoup(res.text, "lxml")
        song_data_area = select_one_tag(bs, "td > div.pure-g > div.pure-u-1 > div:nth-child(1)")

        artist = select_one_tag(song_data_area, "p > a:nth-child(2)")
        artist_link = artist.get("href")
        if not isinstance(artist_link, str):
            raise PetitlyricsLyricPageParserError from ValueError

        m = re.search("(作詞\uff1a|Artist:)(?P<name>[^\u00a0]+)\u00a0", song_data_area.text)
        lyricist = None if m is None else get_captured_value(m, "name")

        m = re.search("(作曲\uff1a|Composer:)(?P<name>[^\u00a0]+)\u00a0", song_data_area.text)
        composer = None if m is None else get_captured_value(m, "name")

        res = sess.get("https://petitlyrics.com/lib/pl-lib.js")
        if not res.ok:
            raise PetitlyricsLyricPageParserError from ConnectionError
        m = re.search(r"'X-CSRF-Token', '(?P<csrf_token>[a-z0-9]{32})'", res.text)

        res_ajax = sess.post(
            "https://petitlyrics.com/com/get_lyrics.ajax",
            data={
                "lyrics_id": pageid,
            },
            headers={
                "X-CSRF-Token": get_captured_value(m, "csrf_token"),
                "X-Requested-With": "XMLHttpRequest",
            },
        )
        if not res_ajax.ok:
            raise PetitlyricsLyricPageParserError from ConnectionError
        bs_ajax = BeautifulSoup(res_ajax.text, "lxml")
        lyric_lines = list(PetitlyricsLyricData.model_validate_json(bs_ajax.text))

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

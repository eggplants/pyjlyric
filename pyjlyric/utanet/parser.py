"""<https://uta-net.com>"""

import re

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.util import (
    get_captured_value,
    get_source,
    parse_obj_as_url,
    parse_text_with_optional_link,
    select_one_tag,
)

from .model import UtanetLyricPage

_UTANET_PATTERN = r"^https://www.uta-net.com/song/(?P<pageid>\d+)/?$"


class UtanetLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class UtanetLyricPageParser(BaseLyricPageParser):
    """https://www.uta-net.com/song/<pageid>"""

    _test = "https://www.uta-net.com/song/155003/"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_UTANET_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> UtanetLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_UTANET_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise UtanetLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise UtanetLyricPageParserError from ConnectionError

        header_div = select_one_tag(bs, "div.song-infoboard")

        artist = select_one_tag(header_div, "a[itemprop='byArtist']")
        artist_link = (
            None
            if artist.href is None
            else parse_obj_as_url(
                artist.href.text,
                base=url,
            )
        )

        composer = select_one_tag(header_div, "a[itemprop='composer']")
        composer_link = (
            None
            if composer.href is None
            else parse_obj_as_url(
                composer.href.text,
                base=url,
            )
        )

        lyricist = select_one_tag(header_div, "a[itemprop='lyricist']")
        lyricist_link = (
            None
            if lyricist.href is None
            else parse_obj_as_url(
                lyricist.href.text,
                base=url,
            )
        )

        arranger = header_div.select_one("a[itemprop='arranger']")
        arranger_link = (
            None
            if arranger is None or arranger.href is None
            else parse_obj_as_url(
                arranger.href.text,
                base=url,
            )
        )

        lyric = select_one_tag(bs, "div#kashi_area")
        for br in lyric.select("br"):
            br.replace_with("\n")

        return UtanetLyricPage(
            title=select_one_tag(header_div, "h2").text,
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=parse_text_with_optional_link(artist.text, artist_link),
            composer=parse_text_with_optional_link(composer.text, composer_link),
            lyricist=parse_text_with_optional_link(lyricist.text, lyricist_link),
            arranger=None if arranger is None else parse_text_with_optional_link(arranger.text, arranger_link),
            lyric_sections=[section.strip().split("\n") for section in lyric.text.replace("\u3000", " ").split("\n\n")],
        )

"""<https://uta-net.com>"""

import re
from urllib.parse import urljoin

from ..base import BaseLyricPageParser, BaseLyricPageParserError
from ..models import LyricPage, WithUrlText
from ..utils import get_captured_value, get_source, parse_obj_as_url, select_one_tag

_UTANET_PATTERN = r"^https://www.uta-net.com/song/(?P<pageid>\d+)/$"


class UtanetLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class UtanetLyricPageParser(BaseLyricPageParser):
    """https://www.uta-net.com/song/<pageid>/"""

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_UTANET_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> LyricPage:
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
                urljoin(url, artist.href.text),
            )
        )

        composer = select_one_tag(header_div, "a[itemprop='composer']")
        composer_link = (
            None
            if composer.href is None
            else parse_obj_as_url(
                urljoin(url, composer.href.text),
            )
        )

        lyricist = select_one_tag(header_div, "a[itemprop='lyricist']")
        lyricist_link = (
            None
            if lyricist.href is None
            else parse_obj_as_url(
                urljoin(url, lyricist.href.text),
            )
        )

        arranger = header_div.select_one("a[itemprop='arranger']")
        arranger_link = (
            None
            if arranger is None or arranger.href is None
            else parse_obj_as_url(
                urljoin(url, arranger.href.text),
            )
        )

        lyric = select_one_tag(bs, "div#kashi_area")
        for br in lyric.select("br"):
            br.replace_with("\n")

        return LyricPage(
            title=select_one_tag(header_div, "h2").text,
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(text=artist.text, link=artist_link),
            composers=[WithUrlText(text=composer.text, link=composer_link)],
            lyricists=[WithUrlText(text=lyricist.text, link=lyricist_link)],
            arrangers=arranger
            if arranger is None
            else [
                WithUrlText(text=arranger.text, link=arranger_link),
            ],
            lyric_sections=[section.strip().split("\n") for section in lyric.text.replace("\u3000", " ").split("\n\n")],
        )

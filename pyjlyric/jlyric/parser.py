"""<https://kashinavi.com>"""

import re
from urllib.parse import urljoin

from ..base import BaseLyricPageParser, BaseLyricPageParserError
from ..models import LyricPage, WithUrlText
from ..utils import get_captured_value, get_source, parse_obj_as_url, select_one_tag

_JLYRIC_PATTERN = r"^https://j-lyric.net/artist/(?P<artistid>[a-z0-9]+)/(?P<pageid>[a-z0-9]+)\.html$"


class JlyricLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class JlyricLyricPageParser(BaseLyricPageParser):
    """https://j-lyric.net/artist/<artistid>/<pageid>.html"""

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_JLYRIC_PATTERN)
        m = re.match(pattern, url)
        artistid = get_captured_value(m, "artistid")
        pageid = get_captured_value(m, "pageid")

        return artistid is not None and pageid is not None

    @staticmethod
    def parse(url: str) -> LyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_JLYRIC_PATTERN)
        m = re.match(pattern, url)
        val = get_captured_value(m, "pageid")
        if val is None:
            raise JlyricLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise JlyricLyricPageParserError from ConnectionError

        title_div = select_one_tag(bs, "#mnb > div.cap")
        title_m = re.match("^「(.*)」歌詞$", title_div.text)
        if title_m is None or len(title_m.groups()) != 1:
            raise JlyricLyricPageParserError from ValueError

        artist = select_one_tag(bs, "#mnb > div.lbdy > p:nth-child(1) > a")
        artist_link = (
            None
            if artist.href is None
            else parse_obj_as_url(
                urljoin(url, artist.href.text),
            )
        )

        composer = select_one_tag(bs, "#mnb > div.lbdy > p:nth-child(2)")
        composer_m = re.match("^作詞\uff1a(.*)$", composer.text)
        if composer_m is None or len(composer_m.groups()) != 1:
            raise JlyricLyricPageParserError from ValueError

        lyricist = select_one_tag(bs, "#mnb > div.lbdy > p:nth-child(3)")
        lyricist_m = re.match("^作曲\uff1a(.*)$", lyricist.text)
        if lyricist_m is None or len(lyricist_m.groups()) != 1:
            raise JlyricLyricPageParserError from ValueError

        lyric = select_one_tag(bs, "#Lyric")
        for br in lyric.select("br"):
            br.replace_with("\n")

        return LyricPage(
            title=title_m.groups()[0],
            page_url=parse_obj_as_url(url),
            pageid=val,
            artist=WithUrlText(link=artist_link, text=artist.text),
            composers=[
                WithUrlText(text=str(composer_name), link=None) for composer_name in composer_m.groups()[0].split("・")
            ],
            lyricists=[
                WithUrlText(text=str(composer_name), link=None) for composer_name in lyricist_m.groups()[0].split("・")
            ],
            arrangers=None,
            lyric_sections=[section.strip().split("\n") for section in lyric.text.replace("\u3000", " ").split("\n\n")],
        )

"""<https://l-lyric.net>"""

import re

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.util import (
    get_captured_value,
    get_source,
    parse_obj_as_url,
    parse_text_with_optional_link,
    select_one_tag,
)

from .model import JlyricLyricPage

_JLYRIC_PATTERN = r"^https://j-lyric\.net/artist/(?P<artistid>[a-z0-9]+)/(?P<pageid>[a-z0-9]+)\.html$"


class JlyricLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class JlyricLyricPageParser(BaseLyricPageParser):
    """https://j-lyric.net/artist/<artistid>/<pageid>.html"""

    _test = "https://j-lyric.net/artist/a05d28d/l05c028.html"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_JLYRIC_PATTERN)
        m = re.match(pattern, url)
        artistid = get_captured_value(m, "artistid")
        pageid = get_captured_value(m, "pageid")

        return artistid is not None and pageid is not None

    @staticmethod
    def parse(url: str) -> JlyricLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_JLYRIC_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
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
                artist.href.text,
                base=url,
            )
        )

        composer = select_one_tag(bs, "#mnb > div.lbdy > p:nth-child(3)")
        composer_m = re.match("^作曲\uff1a(.*)$", composer.text)
        if composer_m is None or len(composer_m.groups()) != 1:
            raise JlyricLyricPageParserError from ValueError

        lyricist = select_one_tag(bs, "#mnb > div.lbdy > p:nth-child(2)")
        lyricist_m = re.match("^作詞\uff1a(.*)$", lyricist.text)
        if lyricist_m is None or len(lyricist_m.groups()) != 1:
            raise JlyricLyricPageParserError from ValueError

        lyric = select_one_tag(bs, "#Lyric")
        for br in lyric.select("br"):
            br.replace_with("\n")

        return JlyricLyricPage(
            title=title_m.groups()[0],
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=parse_text_with_optional_link(artist.text, artist_link),
            composer=composer_m.groups()[0],
            lyricist=lyricist_m.groups()[0],
            arranger=None,
            lyric_sections=[section.strip().split("\n") for section in lyric.text.replace("\u3000", " ").split("\n\n")],
        )

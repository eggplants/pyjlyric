"""<https://music-book.jp>"""

import re

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.model import WithUrlText
from pyjlyric.util import convert_lines_into_sections, get_captured_value, get_source, parse_obj_as_url, select_one_tag

from .model import MusicbookLyricData, MusicbookLyricPage

_MUSICBOOK_PATTERN = r"^https://music-book\.jp/music/Artist/(?P<artistid>\d+)/Music/(?P<pageid>[a-z0-9]+)$"


class MusicbookLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class MusicbookLyricPageParser(BaseLyricPageParser):
    """https://music-book.jp/music/Artist/<artistid>/Music/<pageid>"""

    _test = "https://music-book.jp/music/Artist/1538923/Music/aaahiqc4"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_MUSICBOOK_PATTERN)
        m = re.match(pattern, url)
        artistid = get_captured_value(m, "artistid")
        pageid = get_captured_value(m, "pageid")

        return artistid is not None and pageid is not None

    @staticmethod
    def parse(url: str) -> MusicbookLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_MUSICBOOK_PATTERN)
        m = re.match(pattern, url)
        artistid = get_captured_value(m, "artistid")
        if artistid is None:
            raise MusicbookLyricPageParserError from ValueError

        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise MusicbookLyricPageParserError from ValueError

        bs = get_source(url)
        if bs is None:
            raise MusicbookLyricPageParserError from ConnectionError

        title = select_one_tag(bs, "h1").text

        artist = select_one_tag(bs, "a.text-with-icon.artist")
        artist_name = artist.text.strip()

        m = re.search(r"href=\"(?P<link>/music/Artist/\d+)\"", str(artist))
        artist_link = get_captured_value(m, "link")
        if artist_link is None:
            raise MusicbookLyricPageParserError from ValueError

        lyricist = select_one_tag(bs, "li:nth-child(1) > div > span").text.strip()
        composer = select_one_tag(bs, "li:nth-child(2) > div > span").text.strip()

        bs_lyric = get_source(f"https://music-book.jp/music/Lyrics/Track?artistName={artist_name}&trackTitle={title}")
        if bs_lyric is None:
            raise MusicbookLyricPageParserError from ConnectionError
        lyric_data = MusicbookLyricData.model_validate_json(bs_lyric.text)

        return MusicbookLyricPage(
            title=title,
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(text=artist_name, link=parse_obj_as_url(artist_link, base=url)),
            composer=composer if composer != "-" and not composer else lyric_data.composer,
            lyricist=lyricist if lyricist != "-" and not lyricist else lyric_data.writer,
            arranger=None,
            lyric_sections=convert_lines_into_sections(lyric_data.lyrics),
        )

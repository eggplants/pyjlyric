"""<https://www.joysound.com>"""

import re

from pyjlyric.base import BaseLyricPageParser, BaseLyricPageParserError
from pyjlyric.model import WithUrlText
from pyjlyric.util import get_captured_value, get_source, parse_obj_as_url

from .model import JoysoundLyricData, JoysoundLyricPage

_JOYSOUND_PATTERN = r"^https://www.joysound.com/web/search/song/(?P<pageid>\d+)$"


class JoysoundLyricPageParserError(BaseLyricPageParserError):
    """WIP."""


class JoysoundLyricPageParser(BaseLyricPageParser):
    """https://www.joysound.com/web/search/song/<pageid>"""

    _test = "https://www.joysound.com/web/search/song/112942"

    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Check if the url is valid."""
        pattern = re.compile(_JOYSOUND_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")

        return pageid is not None

    @staticmethod
    def parse(url: str) -> JoysoundLyricPage:
        """Parse the url page and return the result as LyricPage instance."""
        pattern = re.compile(_JOYSOUND_PATTERN)
        m = re.match(pattern, url)
        pageid = get_captured_value(m, "pageid")
        if pageid is None:
            raise JoysoundLyricPageParserError from ValueError

        bs = get_source(
            "https://mspxy.joysound.com/Common/Lyric",
            method="post",
            data={
                "kind": "naviGroupId",
                "selSongNo": pageid,
                "interactionFlg": "0",
                "apiVer": "1.0",
            },
            headers={
                "x-jsp-app-name": "0000800",
            },
        )
        if bs is None:
            raise JoysoundLyricPageParserError from ConnectionError

        track_data = JoysoundLyricData.model_validate_json(bs.text)

        return JoysoundLyricPage(
            title=track_data.song_name,
            page_url=parse_obj_as_url(url),
            pageid=pageid,
            artist=WithUrlText(
                text=track_data.artist_name,
                link=parse_obj_as_url(
                    f"/web/search/artist/{track_data.artist_id}",
                    base=url,
                ),
            ),
            composer=track_data.composer,
            lyricist=track_data.lyricist,
            arranger=None,
            lyric_sections=[line.split("\n") for line in track_data.lyric_list[0].lyric.strip().split("\n\n")],
        )

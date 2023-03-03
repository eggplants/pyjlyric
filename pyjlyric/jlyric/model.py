from typing import Union

from ..model import LyricPage, WithUrlText


class JlyricLyricPage(LyricPage):
    artist: Union[str, WithUrlText]
    composer: str
    lyricist: str
    arranger: None

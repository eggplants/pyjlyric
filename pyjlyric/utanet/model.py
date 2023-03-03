from typing import Union

from ..model import LyricPage, WithUrlText


class UtanetLyricPage(LyricPage):
    artist: Union[str, WithUrlText]
    composer: Union[str, WithUrlText]
    lyricist: Union[str, WithUrlText]
    arranger: Union[None, str, WithUrlText]

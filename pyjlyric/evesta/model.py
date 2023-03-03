from typing import Union

from ..model import LyricPage, WithUrlText


class EvestaLyricPage(LyricPage):
    artist: Union[str, WithUrlText]
    composer: str
    lyricist: str
    arranger: None

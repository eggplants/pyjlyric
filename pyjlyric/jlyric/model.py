from typing import Union

from pyjlyric.model import LyricPage, WithUrlText


class JlyricLyricPage(LyricPage):
    artist: Union[str, WithUrlText]
    composer: str
    lyricist: str
    arranger: None

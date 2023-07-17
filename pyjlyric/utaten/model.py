from typing import Union

from pyjlyric.model import LyricPage, WithUrlText


class UtatenLyricPage(LyricPage):
    artist: Union[str, WithUrlText]
    composer: Union[str, WithUrlText]
    lyricist: Union[str, WithUrlText]
    arranger: Union[None, str, WithUrlText] = None

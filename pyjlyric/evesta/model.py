from __future__ import annotations

from pyjlyric.model import LyricPage, WithUrlText


class EvestaLyricPage(LyricPage):
    artist: str | WithUrlText
    composer: str
    lyricist: str
    arranger: None

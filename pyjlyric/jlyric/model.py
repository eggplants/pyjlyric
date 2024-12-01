from __future__ import annotations

from pyjlyric.model import LyricPage, WithUrlText


class JlyricLyricPage(LyricPage):
    artist: str | WithUrlText
    composer: str
    lyricist: str
    arranger: None

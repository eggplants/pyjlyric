from __future__ import annotations

from pyjlyric.model import LyricPage


class JlyricLyricPage(LyricPage):
    artist: str
    composer: str
    lyricist: str
    arranger: None

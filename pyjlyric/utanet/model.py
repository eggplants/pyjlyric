from __future__ import annotations

from pyjlyric.model import LyricPage, WithUrlText


class UtanetLyricPage(LyricPage):
    artist: str | WithUrlText
    composer: str | WithUrlText
    lyricist: str | WithUrlText
    arranger: None | str | WithUrlText = None

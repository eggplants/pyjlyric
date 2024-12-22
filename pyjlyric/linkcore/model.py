from __future__ import annotations

from pyjlyric.model import LyricPage, WithUrlText


class LinkcoreLyricPage(LyricPage):
    artist: list[str] | WithUrlText | str
    composer: list[str]
    lyricist: list[str]

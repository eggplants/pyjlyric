from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from pyjlyric.model import LyricPage, WithUrlText


class MusicbookLyricPage(LyricPage):
    artist: WithUrlText
    composer: str | None = None
    lyricist: str | None = None
    arranger: None


class MusicbookLyricData(BaseModel):
    title: str | None = None
    writer: str | None = None
    composer: str | None = None
    lyrics: list[str]
    error_code: Literal["apiCallError"] | None = Field(None, alias="errorCode")

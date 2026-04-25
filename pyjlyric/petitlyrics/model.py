from __future__ import annotations

from base64 import standard_b64decode
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, RootModel, field_validator

from pyjlyric.model import LyricPage, WithUrlText


class PetitlyricsLyricPage(LyricPage):
    artist: WithUrlText
    composer: str | None = None
    lyricist: str | None = None
    arranger: None


class _PetitlyricsLyric(BaseModel):
    lyrics: str

    @field_validator("lyrics")
    @classmethod
    def validate_lyrics(cls, v: str) -> str:
        return standard_b64decode(v).decode("utf-8")


def _validate_root(v: list[dict[str, str]]) -> list[str]:
    return [_PetitlyricsLyric(**i).lyrics for i in v]


_PetitlyricsLyricDataDict = Annotated[list[str], BeforeValidator(_validate_root)]


class PetitlyricsLyricData(RootModel[_PetitlyricsLyricDataDict]):
    pass

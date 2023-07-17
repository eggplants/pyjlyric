from base64 import standard_b64decode
from collections.abc import Generator
from typing import Annotated, Dict, List, Optional

from pydantic import BaseModel, BeforeValidator, RootModel, field_validator

from pyjlyric.model import LyricPage, WithUrlText


class PetitlyricsLyricPage(LyricPage):
    artist: WithUrlText
    composer: Optional[str] = None
    lyricist: Optional[str] = None
    arranger: None


class _PetitlyricsLyric(BaseModel):
    lyrics: str

    @field_validator("lyrics")
    @classmethod
    def validate_lyrics(cls, v: str) -> str:
        return standard_b64decode(v).decode("utf-8")


def _validate_root(v: List[Dict[str, str]]) -> List[str]:
    return [_PetitlyricsLyric(**i).lyrics for i in v]


_PetitlyricsLyricDataDict = Annotated[List[str], BeforeValidator(_validate_root)]


class PetitlyricsLyricData(RootModel[_PetitlyricsLyricDataDict]):
    def __iter__(self) -> Generator[str, None, None]:  # type: ignore[override]
        yield from self.root

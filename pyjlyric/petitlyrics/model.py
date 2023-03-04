from base64 import standard_b64decode
from typing import TYPE_CHECKING, List, Optional

from pydantic import BaseModel, validator

from pyjlyric.model import LyricPage, WithUrlText

if TYPE_CHECKING:
    from collections.abc import Generator


class PetitlyricsLyricPage(LyricPage):
    artist: WithUrlText
    composer: Optional[str]
    lyricist: Optional[str]
    arranger: None


class _PetitlyricsLyric(BaseModel):
    lyrics: str

    @validator("lyrics")
    @classmethod
    def validate_lyrics(cls, v: str) -> str:
        return standard_b64decode(v).decode("utf-8")


class PetitlyricsLyricData(BaseModel):
    __root__: List[str]

    @validator("__root__", pre=True, each_item=True)
    @classmethod
    def validate_root(cls, v: dict[str, str]) -> str:
        return _PetitlyricsLyric(**v).lyrics

    def __iter__(self) -> Generator[str, None, None]:  # type: ignore[override]
        yield from self.__root__
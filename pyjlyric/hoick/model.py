from collections.abc import Iterator
from typing import List, Type

from pydantic import BaseModel, validator
from typing_extensions import Self

from pyjlyric.model import LyricPage, WithUrlText


class HoickLyricPage(LyricPage):
    artist: None
    composer: List[WithUrlText]
    lyricist: List[WithUrlText]
    arranger: None


class HoickLyricData(BaseModel):
    __root__: List[str]

    def __iter__(self: Self) -> Iterator[str]:  # type: ignore[override]
        return iter(self.__root__)

    @validator("__root__")
    @classmethod
    def validate(cls: Type[Self], v: List[str]) -> List[str]:  # type: ignore[override]
        return [i for i in v if isinstance(i, str)]

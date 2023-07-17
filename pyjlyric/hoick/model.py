from collections.abc import Iterator
from typing import List, Type

from pydantic import RootModel, field_validator
from typing_extensions import Self

from pyjlyric.model import LyricPage, WithUrlText


class HoickLyricPage(LyricPage):
    artist: None
    composer: List[WithUrlText]
    lyricist: List[WithUrlText]
    arranger: None


class HoickLyricData(RootModel[List[str]]):
    def __iter__(self: Self) -> Iterator[str]:  # type: ignore[override]
        return iter(self.root)

    @field_validator("root")
    @classmethod
    def validate(cls: Type[Self], v: List[str]) -> List[str]:
        return [i for i in v if isinstance(i, str)]

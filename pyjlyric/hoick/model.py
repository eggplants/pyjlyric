from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import RootModel, field_validator
from typing_extensions import Self

from pyjlyric.model import LyricPage, WithUrlText

if TYPE_CHECKING:
    from collections.abc import Iterator


class HoickLyricPage(LyricPage):
    artist: None
    composer: list[WithUrlText]
    lyricist: list[WithUrlText]
    arranger: None


class HoickLyricData(RootModel[list[str]]):
    def __iter__(self: Self) -> Iterator[str]:  # type: ignore[override]
        return iter(self.root)

    @field_validator("root")
    @classmethod
    def validate(cls: type[Self], v: list[str]) -> list[str]:  # type: ignore[override]
        return [i for i in v if isinstance(i, str)]

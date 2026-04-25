from __future__ import annotations

from pydantic import RootModel, field_validator
from typing_extensions import Self

from pyjlyric.model import LyricPage, WithUrlText


class HoickLyricPage(LyricPage):
    artist: None
    composer: list[WithUrlText]
    lyricist: list[WithUrlText]
    arranger: None


class HoickLyricData(RootModel[list[str]]):
    @field_validator("root")
    @classmethod
    def validate_root(cls: type[Self], v: list[str]) -> list[str]:
        return [i for i in v if isinstance(i, str)]

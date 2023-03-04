"""Pydantic models for lyric data."""
from typing import List, Union

from pydantic import BaseModel, HttpUrl


class WithUrlText(BaseModel):
    """WIP."""

    link: HttpUrl
    text: str


_LyricSection = List[str]


class LyricPage(BaseModel):
    """WIP."""

    title: str
    page_url: HttpUrl
    pageid: str

    artist: Union[str, WithUrlText, List[str], List[WithUrlText], None]
    composer: Union[str, WithUrlText, List[str], List[WithUrlText], None]
    lyricist: Union[str, WithUrlText, List[str], List[WithUrlText], None]
    arranger: Union[str, WithUrlText, List[str], List[WithUrlText], None]

    lyric_sections: List[_LyricSection]

"""Pydantic models for lyric data."""
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class WithUrlText(BaseModel):
    """WIP."""

    link: Optional[HttpUrl]
    text: str


_LyricSection = List[str]


class LyricPage(BaseModel):
    """WIP."""

    title: str
    page_url: HttpUrl
    pageid: str

    artist: WithUrlText
    composers: List[WithUrlText]
    lyricists: List[WithUrlText]
    arrangers: Optional[List[WithUrlText]]

    lyric_sections: List[_LyricSection]

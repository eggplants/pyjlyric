"""Pydantic models for lyric data."""

from __future__ import annotations

from pydantic import BaseModel, HttpUrl


class WithUrlText(BaseModel):
    """WIP."""

    link: HttpUrl
    text: str


_LyricSection = list[str]


class LyricPage(BaseModel):
    """WIP."""

    title: str
    page_url: HttpUrl
    pageid: str

    artist: str | WithUrlText | list[str] | list[WithUrlText] | None = None
    composer: str | WithUrlText | list[str] | list[WithUrlText] | None = None
    lyricist: str | WithUrlText | list[str] | list[WithUrlText] | None = None
    arranger: str | WithUrlText | list[str] | list[WithUrlText] | None = None

    lyric_sections: list[_LyricSection]

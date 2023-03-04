from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from ..model import LyricPage, WithUrlText


class MusicbookLyricPage(LyricPage):
    artist: WithUrlText
    composer: Optional[str]
    lyricist: Optional[str]
    arranger: None


class MusicbookLyricData(BaseModel):
    title: Optional[str]
    writer: Optional[str]
    composer: Optional[str]
    lyrics: List[str]
    error_code: Optional[Literal["apiCallError"]] = Field(..., alias="errorCode")

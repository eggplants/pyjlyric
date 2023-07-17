from typing import List, Literal, Optional

from pydantic import BaseModel, Field

from pyjlyric.model import LyricPage, WithUrlText


class MusicbookLyricPage(LyricPage):
    artist: WithUrlText
    composer: Optional[str] = None
    lyricist: Optional[str] = None
    arranger: None


class MusicbookLyricData(BaseModel):
    title: Optional[str] = None
    writer: Optional[str] = None
    composer: Optional[str] = None
    lyrics: List[str]
    error_code: Optional[Literal["apiCallError"]] = Field(None, alias="errorCode")

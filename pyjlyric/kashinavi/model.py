from pydantic import BaseModel, Field, HttpUrl

from pyjlyric.model import LyricPage, WithUrlText


class _ByArtist(BaseModel):
    type_: str = Field(..., alias="@type")
    name_: str
    url: HttpUrl


class _RecordedAs(BaseModel):
    type_: str = Field(..., alias="@type")
    by_artist: _ByArtist = Field(..., alias="byArtist")


class _Lyricist(BaseModel):
    type_: str = Field(..., alias="@type")
    name: str


class _Composer(BaseModel):
    type_: str = Field(..., alias="@type")
    name: str


class _MainEntityOfPage(BaseModel):
    type_: str = Field(..., alias="@type")
    url: HttpUrl


class _Lyrics(BaseModel):
    type_: str = Field(..., alias="@type")
    main_entity_of_page: _MainEntityOfPage = Field(..., alias="mainEntityOfPage")
    text: str


class KashinaviLyricPage(LyricPage):
    artist: WithUrlText
    composer: str
    lyricist: str
    arranger: None

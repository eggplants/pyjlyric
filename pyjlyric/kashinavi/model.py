from pydantic import BaseModel, Field, HttpUrl

from pyjlyric.model import LyricPage, WithUrlText


class _ByArtist(BaseModel):
    _type: str = Field(..., alias="@type")
    name: str
    url: HttpUrl


class _RecordedAs(BaseModel):
    _type: str = Field(..., alias="@type")
    by_artist: _ByArtist = Field(..., alias="byArtist")


class _Lyricist(BaseModel):
    _type: str = Field(..., alias="@type")
    name: str


class _Composer(BaseModel):
    _type: str = Field(..., alias="@type")
    name: str


class _MainEntityOfPage(BaseModel):
    _type: str = Field(..., alias="@type")
    url: HttpUrl


class _Lyrics(BaseModel):
    _type: str = Field(..., alias="@type")
    main_entity_of_page: _MainEntityOfPage = Field(..., alias="mainEntityOfPage")
    text: str


class JSONLD(BaseModel):
    _context: str = Field(..., alias="@context")
    _type: str = Field(..., alias="@type")
    name: str
    recorded_as: _RecordedAs = Field(..., alias="recordedAs")
    lyricist: _Lyricist
    composer: _Composer
    lyrics: _Lyrics = Field(..., alias="Lyrics")


class KashinaviLyricPage(LyricPage):
    artist: WithUrlText
    composer: str
    lyricist: str
    arranger: None

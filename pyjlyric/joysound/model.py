from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from pyjlyric.model import LyricPage, WithUrlText


class JoysoundLyricPage(LyricPage):
    artist: WithUrlText
    composer: Optional[str] = None
    lyricist: Optional[str] = None
    arranger: None


class _LyricListItem(BaseModel):
    service_type: str = Field(..., alias="serviceType")
    service_publish_date: str = Field(..., alias="ServicePublishDate")
    status_code: str = Field(..., alias="statusCode")
    lyric: str


class _ItunesInfo(BaseModel):
    track_id: str = Field(..., alias="trackId")
    song_image_url: str = Field(..., alias="songImageUrl")
    item_url: str = Field(..., alias="itemUrl")
    preview_url: str = Field(..., alias="previewUrl")
    lyricsync_shift_time: str = Field(..., alias="lyricsyncShiftTime")


class _YoutubeInfo(BaseModel):
    movie_id: str = Field(..., alias="movieId")
    lyricsync_shift_time: str = Field(..., alias="lyricsyncShiftTime")
    thumbnail_url: str = Field(..., alias="thumbnailUrl")
    thumbnail_url_medium: str = Field(..., alias="thumbnailUrlMedium")
    thumbnail_url_large: str = Field(..., alias="thumbnailUrlLarge")
    disp_flg: str = Field(..., alias="dispFlg")


class _AmazonInfo(BaseModel):
    song_image_url: str = Field(..., alias="songImageUrl")
    song_image_url_small: str = Field(..., alias="songImageUrlSmall")
    song_image_url_large: str = Field(..., alias="songImageUrlLarge")
    item_name: str = Field(..., alias="itemName")
    item_url: str = Field(..., alias="itemUrl")


class _WikipediaInfo(BaseModel):
    item_url: str = Field(..., alias="itemUrl")
    official_url: str = Field(..., alias="officialUrl")
    twitter_account: str = Field(..., alias="twitterAccount")
    facebook_account: str = Field(..., alias="facebookAccount")


class _Field121centerInfo(BaseModel):
    song_image_url: str = Field(..., alias="songImageUrl")
    artist_image_url: str = Field(..., alias="artistImageUrl")


class _OutsideUrlInfo(BaseModel):
    itunes_info: _ItunesInfo = Field(..., alias="itunesInfo")
    youtube_info: _YoutubeInfo = Field(..., alias="youtubeInfo")
    amazon_info: _AmazonInfo = Field(..., alias="amazonInfo")
    wikipedia_info: _WikipediaInfo = Field(..., alias="wikipediaInfo")
    jsm_info: List[str] = Field(..., alias="jsmInfo")
    field_121center_info: _Field121centerInfo = Field(..., alias="121centerInfo")


class JoysoundLyricData(BaseModel):
    navi_group_id: str = Field(..., alias="naviGroupId")
    song_id: str = Field(..., alias="songId")
    sel_song_no: str = Field(..., alias="selSongNo")
    song_name: str = Field(..., alias="songName")
    song_name_ruby: str = Field(..., alias="songNameRuby")
    song_name_ruby_sort: str = Field(..., alias="songNameRubySort")
    song_name_alphabet: str = Field(..., alias="songNameAlphabet")
    song_name_alphabet_search_sort: str = Field(..., alias="songNameAlphabetSearchSort")
    song_name_japanese: str = Field(..., alias="songNameJapanese")
    song_name_japanese_ruby: str = Field(..., alias="songNameJapaneseRuby")
    song_name_japanese_sort: str = Field(..., alias="songNameJapaneseSort")
    song_name_foreign: str = Field(..., alias="songNameForeign")
    song_name_foreign_search: str = Field(..., alias="songNameForeignSearch")
    song_name_foreign_sort: str = Field(..., alias="songNameForeignSort")
    lyricist: str
    composer: str
    artist_id: str = Field(..., alias="artistId")
    group_artist_id: str = Field(..., alias="groupArtistId")
    artist_seq: str = Field(..., alias="artistSeq")
    artist_name: str = Field(..., alias="artistName")
    artist_name_ruby: str = Field(..., alias="artistNameRuby")
    artist_name_ruby_sort: str = Field(..., alias="artistNameRubySort")
    artist_name_alphabet_search_sort: str = Field(..., alias="artistNameAlphabetSearchSort")
    artist_name_foreign: str = Field(..., alias="artistNameForeign")
    artist_name_foreign_search: str = Field(..., alias="artistNameForeignSearch")
    artist_name_foreign_sort: str = Field(..., alias="artistNameForeignSort")
    artist_dv: str = Field(..., alias="artistDv")
    myartist_flg: str = Field(..., alias="myartistFlg")
    lyric_list: List[_LyricListItem] = Field(..., alias="lyricList")
    outside_url_info: _OutsideUrlInfo = Field(..., alias="outsideUrlInfo")

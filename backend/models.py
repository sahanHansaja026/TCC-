from pydantic import BaseModel, HttpUrl
from typing import Optional

class YouTubeURL(BaseModel):
    url: HttpUrl

class VideoMetadata(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    publish_date: Optional[str] = None
    duration: Optional[str] = None
    views: Optional[int] = None
    author: Optional[str] = None
    thumbnail_url: Optional[str] = None
    summary: Optional[str] = None
    transcript: Optional[str] = None
    transcript_available: bool = False

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    text: str

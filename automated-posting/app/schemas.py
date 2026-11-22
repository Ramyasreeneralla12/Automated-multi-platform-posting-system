import re
from datetime import datetime
from typing import Literal, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator, ConfigDict

URL_PATTERN = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)

class PostingRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=200)

    @field_validator("message")
    @classmethod
    def validate_message_and_cta(cls, value: str) -> str:
        urls = URL_PATTERN.findall(value)
        if len(urls) != 1:
            raise ValueError("Message must contain exactly one CTA URL")
        parsed = urlparse(urls[0].rstrip(".,);]"))
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError("CTA URL must be a valid HTTP or HTTPS URL")
        if "." not in parsed.hostname and parsed.hostname != "localhost":
            raise ValueError("CTA URL must contain a valid hostname")
        return value

class PlatformResult(BaseModel):
    platform: str
    status: Literal["success", "failed"]
    posted_url: Optional[str] = None
    public_access: bool = False
    date: Optional[str] = None
    time: Optional[str] = None
    error: Optional[str] = None

class PostingResponse(BaseModel):
    success: bool
    results: list[PlatformResult]

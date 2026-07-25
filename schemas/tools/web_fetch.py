from pydantic import BaseModel, Field, HttpUrl


class WebFetchInput(BaseModel):
    url: HttpUrl
    timeout_seconds: int = Field(default=10, ge=1, le=60)


class WebFetchOutput(BaseModel):
    url: str
    title: str | None
    content: str
    word_count: int
    success: bool
    error: str | None = None

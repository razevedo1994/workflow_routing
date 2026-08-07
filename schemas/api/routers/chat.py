from pydantic import BaseModel
from router.content_type import ContentType


class ChatRequest(BaseModel):
    message: str
    content_type: ContentType = ContentType.TEXT
    session_id: str | None = None

class ChatResponde(BaseModel):
    session_id: str
    intent: str
    steps: list[str]
    result: dict
    error: str | None = None

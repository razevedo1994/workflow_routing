from pydantic import BaseModel, Field
from router.content_type import ContentType


class SummarizerInput(BaseModel):
    content: str
    content_type: ContentType
    focus: str | None = Field(
        default=None,
        description="Optional: 'methodology', 'results', 'conclusions', etc.",
    )


class SummaryOutput(BaseModel):
    title: str = Field(description="Title or inferred topic")
    key_points: list[str] = Field(description="3-7 main points")
    conclusion: str = Field(description="Author's final position or finding")
    gaps: list[str] = Field(description="What the source does NOT cover")
    confidence: float = Field(description="0.0 to 1.0 - how complete the summary is")

from typing import Literal, Optional

from pydantic import BaseModel, Field


class RoutingDecision(BaseModel):
    agent_type: Literal[
        "summarizer_agent", "critic_agent", "comparison_agent", "extractor_agent"
    ] = Field(description="Type of agent chosen for the task.")
    confidence: float = Field(description="Confidence score between 0 and 1")
    description: str = Field(description="Clean description of the request")
    focus: Optional[str] = Field(
        default=None,
        description="If the user asked to focus on a specific aspect (e.g. 'methodology', 'results', 'conclusions'), extract it here; otherwise None.",
    )
    reasoning: Optional[str] = Field(default=None, description="Explanation of the decision.")

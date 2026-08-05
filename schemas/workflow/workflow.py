from typing import Any

from pydantic import BaseModel, Field


class WorkflowResult(BaseModel):
    intent: str
    steps: list[str] = Field(default_factory=list)
    outputs: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None

    model_config = {"arbitrary_types_allowed": True}

    @property
    def success(self) -> bool:
        return self.error is None

    def add(self, step: str, output: Any) -> None:
        self.steps.append(step)
        self.outputs[step] = output

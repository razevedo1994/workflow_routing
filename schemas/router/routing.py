from typing import Literal, Optional

from pydantic import BaseModel, Field


class RoutingDecision(BaseModel):
    agent_type: Literal[
        "summarizer_agent", "critic_agent", "comparison_agent", "extractor_agent"
    ] = Field(description="Tipo de agente escolhido para a tarefa.")
    confidence: float = Field(description="Pontuação de confiança entre 0 e 1")
    description: str = Field(description="Descrição limpa da solicitação")
    focus: Optional[str] = Field(
        default=None,
        description="If the user asked to focus on a specific aspect (e.g. 'methodology', 'results', 'conclusions'), extract it here; otherwise None.",
    )
    reasoning: Optional[str] = Field(default=None, description="Explicação da decisão.")

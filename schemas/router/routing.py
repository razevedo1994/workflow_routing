from typing import Literal, Optional

from pydantic import BaseModel, Field


class RoutingDecision(BaseModel):
    agent_type: Literal["agente_1", "agente_2", "agente_3"] = Field(
        description="Tipo de agente escolhido para a tarefa."
    )
    confidence: float = Field(description="Pontuação de confiança entre 0 e 1")
    description: str = Field(description="Descrição limpa da solicitação")
    reasoning: Optional[str] = Field(default=None, description="Explicação da decisão.")

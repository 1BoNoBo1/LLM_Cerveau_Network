# api/schemas/agent_schema.py
# Schémas Pydantic pour les requêtes/réponses de l'API

from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ModeReflexion(str, Enum):
    """Mode de réflexion du cerveau."""
    COMPLET = "complet"  # 4 agents : Initiateur -> Créatif -> Critique -> Synthétiseur
    RAPIDE = "rapide"    # 2 agents : Initiateur -> Synthétiseur


class AgentRequest(BaseModel):
    """Requête pour lancer une réflexion."""
    message: str = Field(
        ...,
        description="La question ou le problème à analyser",
        min_length=1,
        max_length=5000,
    )
    mode: ModeReflexion = Field(
        default=ModeReflexion.COMPLET,
        description="Mode de réflexion : 'complet' (4 agents) ou 'rapide' (2 agents)",
    )


class AgentResponse(BaseModel):
    """Réponse du cerveau après réflexion."""
    question: str = Field(description="La question originale")
    synthese: str = Field(description="La réponse synthétisée")
    succes: bool = Field(description="Indique si la réflexion s'est bien déroulée")
    mode: str = Field(description="Mode de réflexion utilisé")


class HealthResponse(BaseModel):
    """Réponse du health check."""
    status: str
    message: str
    agents_disponibles: list[str]

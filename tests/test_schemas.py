# tests/test_schemas.py
# Tests pour les schémas Pydantic

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api"))

import pytest
from pydantic import ValidationError


class TestAgentRequest:
    """Tests pour le schéma AgentRequest."""

    def test_valid_request(self):
        """Test une requête valide."""
        from api.schemas.agent_schema import AgentRequest

        request = AgentRequest(message="Test question")

        assert request.message == "Test question"
        assert request.mode.value == "complet"  # défaut

    def test_request_with_mode(self):
        """Test une requête avec mode spécifié."""
        from api.schemas.agent_schema import AgentRequest, ModeReflexion

        request = AgentRequest(message="Test", mode=ModeReflexion.RAPIDE)

        assert request.mode == ModeReflexion.RAPIDE

    def test_empty_message_rejected(self):
        """Test qu'un message vide est rejeté."""
        from api.schemas.agent_schema import AgentRequest

        with pytest.raises(ValidationError):
            AgentRequest(message="")

    def test_message_too_long_rejected(self):
        """Test qu'un message trop long est rejeté."""
        from api.schemas.agent_schema import AgentRequest

        with pytest.raises(ValidationError):
            AgentRequest(message="x" * 5001)  # max 5000

    def test_invalid_mode_rejected(self):
        """Test qu'un mode invalide est rejeté."""
        from api.schemas.agent_schema import AgentRequest

        with pytest.raises(ValidationError):
            AgentRequest(message="Test", mode="invalide")


class TestAgentResponse:
    """Tests pour le schéma AgentResponse."""

    def test_valid_response(self):
        """Test une réponse valide."""
        from api.schemas.agent_schema import AgentResponse

        response = AgentResponse(
            question="Test?",
            synthese="Réponse",
            succes=True,
            mode="complet"
        )

        assert response.question == "Test?"
        assert response.synthese == "Réponse"
        assert response.succes is True
        assert response.mode == "complet"


class TestHealthResponse:
    """Tests pour le schéma HealthResponse."""

    def test_valid_health(self):
        """Test une réponse health valide."""
        from api.schemas.agent_schema import HealthResponse

        health = HealthResponse(
            status="ok",
            message="Système opérationnel",
            agents_disponibles=["Agent1", "Agent2"]
        )

        assert health.status == "ok"
        assert len(health.agents_disponibles) == 2


class TestModeReflexion:
    """Tests pour l'enum ModeReflexion."""

    def test_modes_disponibles(self):
        """Test que les modes sont bien définis."""
        from api.schemas.agent_schema import ModeReflexion

        assert ModeReflexion.COMPLET.value == "complet"
        assert ModeReflexion.RAPIDE.value == "rapide"

    def test_mode_from_string(self):
        """Test la création depuis une string."""
        from api.schemas.agent_schema import ModeReflexion

        mode = ModeReflexion("complet")
        assert mode == ModeReflexion.COMPLET

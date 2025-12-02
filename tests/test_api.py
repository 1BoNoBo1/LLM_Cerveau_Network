# tests/test_api.py
# Tests pour l'API FastAPI

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "api"))

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Crée un client de test pour l'API."""
    from api.main import app
    return TestClient(app)


class TestRootEndpoint:
    """Tests pour l'endpoint racine."""

    def test_root_returns_info(self, client):
        """Test que la racine retourne les infos de l'API."""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "nom" in data
        assert data["nom"] == "LLM Cerveau Network"
        assert "version" in data
        assert "endpoints" in data


class TestHealthEndpoint:
    """Tests pour l'endpoint de santé."""

    def test_health_endpoint_exists(self, client):
        """Test que l'endpoint health existe."""
        response = client.get("/api/health")

        # Peut retourner 200 (OK) ou 500 (si Ollama non disponible)
        assert response.status_code in [200, 500]

    def test_health_response_format(self, client):
        """Test le format de la réponse health."""
        response = client.get("/api/health")
        data = response.json()

        assert "status" in data
        assert "message" in data
        assert "agents_disponibles" in data


class TestPenserEndpoint:
    """Tests pour l'endpoint /penser."""

    def test_penser_requires_message(self, client):
        """Test que le message est requis."""
        response = client.post("/api/penser", json={})

        assert response.status_code == 422  # Validation error

    def test_penser_accepts_valid_request(self, client):
        """Test qu'une requête valide est acceptée."""
        # Note: Ce test peut échouer si Ollama n'est pas disponible
        response = client.post(
            "/api/penser",
            json={
                "message": "Test question",
                "mode": "rapide"
            }
        )

        # 200 si Ollama disponible, 500 sinon
        assert response.status_code in [200, 500]

    def test_penser_mode_validation(self, client):
        """Test la validation du mode."""
        response = client.post(
            "/api/penser",
            json={
                "message": "Test",
                "mode": "mode_invalide"
            }
        )

        assert response.status_code == 422


class TestRunAgentEndpoint:
    """Tests pour l'endpoint legacy /run_agent."""

    def test_run_agent_exists(self, client):
        """Test que l'endpoint legacy existe."""
        response = client.post(
            "/api/run_agent",
            json={"message": "Test"}
        )

        # Doit exister (peut échouer pour autres raisons)
        assert response.status_code in [200, 500, 422]


class TestAPIDocumentation:
    """Tests pour la documentation de l'API."""

    def test_docs_available(self, client):
        """Test que la documentation Swagger est disponible."""
        response = client.get("/docs")

        assert response.status_code == 200

    def test_redoc_available(self, client):
        """Test que ReDoc est disponible."""
        response = client.get("/redoc")

        assert response.status_code == 200

    def test_openapi_schema(self, client):
        """Test que le schéma OpenAPI est disponible."""
        response = client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()

        assert "info" in data
        assert data["info"]["title"] == "LLM Cerveau Network API"

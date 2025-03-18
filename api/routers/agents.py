from fastapi import APIRouter, HTTPException
from schemas.agent_schema import AgentRequest, AgentResponse
import autogen
import logging

# Configuration du logging pour voir les messages de debug
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# Exemple de configuration pour illustrer plusieurs agents (vous pouvez l'adapter selon vos besoins)
config_list = [
    {
        "base_url": "http://localhost:11434/v1",
        "model": "gemma:2b",
    },
    {
        "base_url": "http://localhost:11434/v1",
        "model": "phi:2",
    }
]

# Définition de l'agent initiateur avec une configuration vers ollama
logger.info("Configuration de l'agent initiateur avec ollama")
logger.info("Base URL: http://localhost:11434")
logger.info("Model: gemma-2b")

initiator = autogen.AssistantAgent(
    name="Initiateur",
    llm_config={
        "type": "ollama",
        "base_url": "http://localhost:11434",
        "model": "gemma-2b",
    }
)

logger.info(f"Agent initiateur configuré: {initiator.llm_config}")

@router.post("/run_agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    user_message = request.message

    try:
        response = initiator.generate_reply(
            messages=[{"role": "user", "content": user_message}]
        )
        logger.info(f"Réponse générée avec succès pour le message: {user_message}")
        return {"response": response}
    except Exception as e:
        logger.error(f"Erreur lors de la génération de la réponse pour le message: {user_message}. Erreur: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

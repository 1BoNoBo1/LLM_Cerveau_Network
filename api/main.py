# api/main.py
# Point d'entrée de l'API LLM Cerveau Network

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.agents import router as agent_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LLM Cerveau Network API",
    description="""
## Cerveau collaboratif multi-agents

Un système d'IA distribuée où 4 agents LLM spécialisés collaborent :

- **Initiateur** : Analyse et structure le problème
- **Créatif** : Propose des idées originales
- **Critique** : Évalue forces et faiblesses
- **Synthétiseur** : Crée la réponse finale

### Modes de réflexion

- `complet` : Les 4 agents collaborent (plus approfondi)
- `rapide` : Initiateur + Synthétiseur uniquement (plus rapide)
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS pour permettre les appels depuis un frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routes
app.include_router(agent_router, prefix="/api", tags=["Cerveau Network"])


@app.get("/")
async def root():
    """Page d'accueil de l'API."""
    return {
        "nom": "LLM Cerveau Network",
        "version": "2.0.0",
        "description": "Cerveau collaboratif multi-agents",
        "documentation": "/docs",
        "endpoints": {
            "penser": "POST /api/penser - Lance une réflexion collaborative",
            "health": "GET /api/health - Vérifie l'état du système",
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# api/routers/agents.py
# Endpoints pour interagir avec le Cerveau Network

import sys
import os
import logging

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

# Ajouter le répertoire parent au path pour importer agents
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from schemas.agent_schema import (
    AgentRequest,
    AgentResponse,
    HealthResponse,
    ModeReflexion,
)
from agents.cerveau import get_cerveau
from agents.memory import get_memoire

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Vérifie l'état du Cerveau Network."""
    try:
        cerveau = get_cerveau()
        return HealthResponse(
            status="ok",
            message="Cerveau Network opérationnel",
            agents_disponibles=["Initiateur", "Créatif", "Critique", "Synthétiseur"],
        )
    except Exception as e:
        logger.error(f"Erreur health check: {e}")
        return HealthResponse(
            status="error",
            message=str(e),
            agents_disponibles=[],
        )


@router.post("/penser", response_model=AgentResponse)
async def penser(request: AgentRequest):
    """
    Lance une réflexion collaborative du Cerveau Network.

    - **message** : La question ou le problème à analyser
    - **mode** : 'complet' (4 agents) ou 'rapide' (2 agents)

    Retourne la synthèse de la réflexion collective.
    """
    logger.info(f"Nouvelle requête reçue - Mode: {request.mode.value}")

    try:
        cerveau = get_cerveau()

        if request.mode == ModeReflexion.RAPIDE:
            resultat = cerveau.penser_rapide(request.message)
        else:
            resultat = cerveau.penser(request.message)

        return AgentResponse(
            question=resultat["question"],
            synthese=resultat["synthese"],
            succes=resultat["succes"],
            mode=request.mode.value,
        )

    except Exception as e:
        logger.error(f"Erreur lors de la réflexion: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la réflexion: {str(e)}",
        )


@router.get("/memoire/stats")
async def stats_memoire():
    """
    Retourne les statistiques de la mémoire du cerveau.

    - Nombre de conversations stockées
    - Nombre de contextes permanents
    """
    try:
        memoire = get_memoire()
        return memoire.stats()
    except Exception as e:
        logger.error(f"Erreur stats mémoire: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/memoire/rechercher")
async def rechercher_memoire(
    q: str = Query(..., description="Texte de recherche"),
    k: int = Query(5, ge=1, le=20, description="Nombre de résultats"),
    mode: Optional[str] = Query(None, description="Filtrer par mode (complet/rapide)")
):
    """
    Recherche dans la mémoire des conversations passées.

    - **q** : Texte de recherche
    - **k** : Nombre de résultats (1-20)
    - **mode** : Filtrer par mode de réflexion
    """
    try:
        memoire = get_memoire()
        resultats = memoire.rechercher(q, k=k, filtre_mode=mode)
        return {"resultats": resultats, "total": len(resultats)}
    except Exception as e:
        logger.error(f"Erreur recherche mémoire: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/memoire/effacer")
async def effacer_memoire(confirmer: bool = Query(False, description="Confirmer l'effacement")):
    """
    Efface toute la mémoire du cerveau.

    **ATTENTION** : Cette action est irréversible !

    - **confirmer** : Doit être True pour confirmer l'effacement
    """
    if not confirmer:
        raise HTTPException(
            status_code=400,
            detail="Ajoutez ?confirmer=true pour confirmer l'effacement"
        )

    try:
        memoire = get_memoire()
        memoire.effacer(confirmer=True)
        return {"message": "Mémoire effacée avec succès"}
    except Exception as e:
        logger.error(f"Erreur effacement mémoire: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Garder l'ancien endpoint pour compatibilité
@router.post("/run_agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    """
    [DEPRECATED] Utilisez /penser à la place.
    Cet endpoint est maintenu pour compatibilité.
    """
    return await penser(request)

# agents/config.py
# Configuration des modèles LLM pour chaque agent

import os
from dotenv import load_dotenv

load_dotenv()

# Configuration Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Modèles recommandés pour GTX 1650 4GB
# Vous pouvez changer ces valeurs selon vos modèles installés
MODELES = {
    "initiateur": os.getenv("MODEL_INITIATEUR", "qwen2.5:3b"),
    "creatif": os.getenv("MODEL_CREATIF", "qwen2.5:3b"),
    "critique": os.getenv("MODEL_CRITIQUE", "qwen2.5:3b"),
    "synthetiseur": os.getenv("MODEL_SYNTHETISEUR", "qwen2.5:3b"),
}

# Fallback si qwen2.5 n'est pas disponible
MODELE_FALLBACK = os.getenv("MODEL_FALLBACK", "gemma:2b")

# Configuration du timeout (en secondes)
TIMEOUT_AGENT = int(os.getenv("TIMEOUT_AGENT", "120"))

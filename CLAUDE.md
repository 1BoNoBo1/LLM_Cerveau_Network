# CLAUDE.md - Guide pour LLM Cerveau Network

## Vue d'ensemble

**LLM Cerveau Network** est un système d'IA distribuée où 4 agents LLM spécialisés collaborent comme des "neurones" pour résoudre des problèmes. Orchestré par **CrewAI** avec des modèles locaux via **Ollama**.

**Langage :** Français (docs/commentaires), Python (code)
**Licence :** MIT

## Architecture

```
LLM-Cerveau-Network/
├── agents/                 # Module des agents spécialisés
│   ├── __init__.py
│   ├── config.py          # Configuration des modèles
│   └── cerveau.py         # Orchestration CrewAI
├── api/                    # API REST FastAPI
│   ├── main.py            # Point d'entrée FastAPI
│   ├── routers/
│   │   └── agents.py      # Endpoints /penser, /health
│   └── schemas/
│       └── agent_schema.py # Schémas Pydantic
├── scripts/
│   └── setup.sh           # Script d'installation
├── .env.example           # Variables d'environnement
├── requirements.txt       # Dépendances Python
└── README.md
```

## Les 4 Agents

| Agent | Rôle | Description |
|-------|------|-------------|
| **Initiateur** | Analyse | Décompose le problème, lance la réflexion |
| **Créatif** | Idéation | Propose des idées originales et innovantes |
| **Critique** | Évaluation | Analyse forces/faiblesses, suggère améliorations |
| **Synthétiseur** | Fusion | Crée une réponse finale cohérente |

## Stack Technique

| Composant | Technologie |
|-----------|-------------|
| Orchestration | CrewAI |
| LLMs locaux | Ollama (qwen2.5:3b recommandé) |
| API | FastAPI + Uvicorn |
| Validation | Pydantic |
| Base vectorielle | ChromaDB (future) |

## Installation

### Prérequis
- Python 3.10+
- Ollama installé et lancé
- GPU recommandé (GTX 1650 4GB minimum)

### Installation rapide
```bash
# Cloner et entrer dans le projet
git clone https://github.com/1BoNoBo1/LLM_Cerveau_Network.git
cd LLM_Cerveau_Network

# Créer l'environnement virtuel
python3 -m venv llm_env
source llm_env/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Télécharger le modèle recommandé
ollama pull qwen2.5:3b

# Copier et configurer l'environnement
cp .env.example .env
```

### Lancer l'API
```bash
source llm_env/bin/activate
cd api
uvicorn main:app --reload
```

API disponible sur `http://localhost:8000`
Documentation interactive : `http://localhost:8000/docs`

## Utilisation de l'API

### Endpoint principal : POST /api/penser

```bash
# Mode complet (4 agents)
curl -X POST http://localhost:8000/api/penser \
  -H "Content-Type: application/json" \
  -d '{"message": "Comment améliorer la productivité au travail?", "mode": "complet"}'

# Mode rapide (2 agents)
curl -X POST http://localhost:8000/api/penser \
  -H "Content-Type: application/json" \
  -d '{"message": "Quelle est la capitale de la France?", "mode": "rapide"}'
```

### Réponse type
```json
{
  "question": "Comment améliorer la productivité au travail?",
  "synthese": "Réponse synthétisée par les 4 agents...",
  "succes": true,
  "mode": "complet"
}
```

## Configuration

### Variables d'environnement (.env)
```bash
OLLAMA_BASE_URL=http://localhost:11434
MODEL_INITIATEUR=qwen2.5:3b
MODEL_CREATIF=qwen2.5:3b
MODEL_CRITIQUE=qwen2.5:3b
MODEL_SYNTHETISEUR=qwen2.5:3b
TIMEOUT_AGENT=120
```

### Modèles recommandés par GPU

| GPU | VRAM | Modèle recommandé |
|-----|------|-------------------|
| GTX 1650 | 4GB | qwen2.5:3b, gemma:2b |
| RTX 3060 | 12GB | qwen2.5:7b, phi3 |
| RTX 4090 | 24GB | qwen2.5:14b, deepseek-r1:8b |

## Conventions de Code

### Style Python
- Type hints avec Pydantic
- Logging via `logging` module
- Commentaires en français
- Patterns FastAPI pour l'API

### Structure des imports
```python
# Dans api/main.py
from routers.agents import router as agent_router

# Dans api/routers/agents.py
from schemas.agent_schema import AgentRequest, AgentResponse
from agents.cerveau import get_cerveau
```

## Tests

```bash
# Lancer les tests
pytest tests/

# Test manuel de l'API
curl http://localhost:8000/api/health
```

## Développement

### Modifier le comportement des agents

Éditer `agents/cerveau.py` :
- `_creer_initiateur()` : Personnalité de l'agent Initiateur
- `_creer_creatif()` : Style créatif
- `_creer_critique()` : Critères d'analyse
- `_creer_synthetiseur()` : Méthode de synthèse

### Ajouter un nouvel endpoint

1. Ajouter le schéma dans `api/schemas/agent_schema.py`
2. Ajouter la route dans `api/routers/agents.py`
3. Documenter dans ce fichier

## Sécurité

- Ne jamais commiter `.env`
- Ne pas exposer l'API sur internet sans authentification
- Les modèles restent locaux (Ollama)

## Dépannage

### Ollama ne répond pas
```bash
# Vérifier qu'Ollama est lancé
ollama list

# Relancer si nécessaire
ollama serve
```

### Modèle non trouvé
```bash
# Télécharger le modèle
ollama pull qwen2.5:3b
```

### Mémoire GPU insuffisante
- Utiliser des modèles plus petits (gemma:2b)
- Ou configurer un seul modèle pour tous les agents

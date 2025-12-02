# CLAUDE.md - Guide pour LLM Cerveau Network

## Vue d'ensemble

**LLM Cerveau Network** est un système d'IA distribuée où 4 agents LLM spécialisés collaborent comme des "neurones" pour résoudre des problèmes. Orchestré par **CrewAI** avec des modèles locaux via **Ollama**, et doté d'une mémoire persistante via **ChromaDB**.

**Langage :** Français (docs/commentaires), Python (code)
**Licence :** MIT

## Architecture

```
LLM-Cerveau-Network/
├── agents/                 # Module des agents spécialisés
│   ├── __init__.py
│   ├── config.py          # Configuration des modèles
│   ├── cerveau.py         # Orchestration CrewAI
│   └── memory.py          # Mémoire ChromaDB
├── api/                    # API REST FastAPI
│   ├── main.py            # Point d'entrée FastAPI
│   ├── routers/
│   │   └── agents.py      # Endpoints
│   └── schemas/
│       └── agent_schema.py # Schémas Pydantic
├── ui/                     # Interface utilisateur
│   └── app.py             # Application Streamlit
├── tests/                  # Tests automatisés
│   ├── conftest.py        # Fixtures pytest
│   ├── test_memory.py     # Tests mémoire
│   ├── test_api.py        # Tests API
│   └── test_schemas.py    # Tests schémas
├── data/                   # Base vectorielle (gitignored)
│   └── chromadb/          # Stockage ChromaDB
├── scripts/
│   └── setup.sh
├── .env.example
├── requirements.txt
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
| Mémoire | ChromaDB (base vectorielle) |
| Interface | Streamlit |
| Validation | Pydantic |
| Tests | pytest + httpx |

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

## Lancer l'Application

### Option 1 : API FastAPI
```bash
source llm_env/bin/activate
cd api
uvicorn main:app --reload
```
- API : `http://localhost:8000`
- Documentation : `http://localhost:8000/docs`

### Option 2 : Interface Streamlit
```bash
source llm_env/bin/activate
streamlit run ui/app.py
```
- Interface : `http://localhost:8501`

## API Endpoints

### Réflexion

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/penser` | Lance une réflexion (complet/rapide) |
| GET | `/api/health` | Vérifie l'état du système |

### Mémoire

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/memoire/stats` | Statistiques de la mémoire |
| GET | `/api/memoire/rechercher?q=...` | Recherche dans l'historique |
| DELETE | `/api/memoire/effacer?confirmer=true` | Efface la mémoire |

### Exemples d'utilisation

```bash
# Mode complet (4 agents)
curl -X POST http://localhost:8000/api/penser \
  -H "Content-Type: application/json" \
  -d '{"message": "Comment améliorer la productivité?", "mode": "complet"}'

# Mode rapide (2 agents)
curl -X POST http://localhost:8000/api/penser \
  -H "Content-Type: application/json" \
  -d '{"message": "Capitale de la France?", "mode": "rapide"}'

# Rechercher dans la mémoire
curl "http://localhost:8000/api/memoire/rechercher?q=productivité&k=5"

# Stats mémoire
curl http://localhost:8000/api/memoire/stats
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

## Tests

```bash
# Lancer tous les tests
pytest tests/ -v

# Tests spécifiques
pytest tests/test_memory.py -v
pytest tests/test_api.py -v
pytest tests/test_schemas.py -v

# Avec couverture
pytest tests/ --cov=agents --cov=api
```

## Fonctionnalités

### Mémoire Persistante (ChromaDB)
- Sauvegarde automatique des conversations
- Recherche sémantique dans l'historique
- Contexte des conversations passées fourni aux agents
- Stockage dans `data/chromadb/`

### Interface Streamlit
- Mode complet ou rapide
- Historique de session
- Recherche dans la mémoire
- Affichage des statistiques

### Modes de Réflexion

| Mode | Agents | Temps estimé | Usage |
|------|--------|--------------|-------|
| `complet` | 4 agents | ~2 min | Problèmes complexes |
| `rapide` | 2 agents | ~30 sec | Questions simples |

## Développement

### Modifier le comportement des agents
Éditer `agents/cerveau.py` :
- `_creer_initiateur()` : Personnalité de l'Initiateur
- `_creer_creatif()` : Style créatif
- `_creer_critique()` : Critères d'analyse
- `_creer_synthetiseur()` : Méthode de synthèse

### Ajouter un endpoint
1. Ajouter le schéma dans `api/schemas/agent_schema.py`
2. Ajouter la route dans `api/routers/agents.py`
3. Ajouter les tests dans `tests/test_api.py`

### Structure des imports
```python
# Dans api/main.py
from routers.agents import router as agent_router

# Dans api/routers/agents.py
from schemas.agent_schema import AgentRequest, AgentResponse
from agents.cerveau import get_cerveau
from agents.memory import get_memoire
```

## Sécurité

- Ne jamais commiter `.env`
- Ne pas exposer l'API sur internet sans authentification
- Les modèles restent locaux (Ollama)
- Le dossier `data/` est gitignored

## Dépannage

### Ollama ne répond pas
```bash
ollama list      # Vérifier les modèles
ollama serve     # Relancer si nécessaire
```

### Modèle non trouvé
```bash
ollama pull qwen2.5:3b
```

### Mémoire GPU insuffisante
- Utiliser des modèles plus petits (gemma:2b)
- Ou configurer un seul modèle pour tous les agents

### Erreur ChromaDB
```bash
rm -rf data/chromadb  # Reset la base (perte des données)
```

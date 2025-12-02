# CLAUDE.md - AI Assistant Guide for LLM Cerveau Network

## Project Overview

**LLM Cerveau Network** is an experimental distributed artificial intelligence system where multiple quantized LLM models act as specialized "neurons" that communicate and reason together. The project orchestrates agent interactions via AutoGen and runs local models through Ollama, optimized for modest hardware (GTX 1650 4GB).

**Primary Language:** French (documentation and comments), Python (code)
**License:** MIT

## Architecture

```
LLM-Cerveau-Network/
├── api/                    # FastAPI REST API
│   ├── main.py            # FastAPI app entry point
│   ├── routers/
│   │   └── agents.py      # Agent interaction endpoints
│   └── schemas/
│       └── agent_schema.py # Pydantic request/response models
├── scripts/
│   └── setup.sh           # Interactive setup script (Bash)
├── requirements.txt        # Python dependencies
├── .gitignore
├── LICENSE
└── README.md
```

### Planned Directories (not yet created)
- `agents/` - Specialized agent definitions
- `docker/` - Docker and Docker Compose files
- `models/` - Local LLM model storage (gitignored)
- `data/` - ChromaDB vector database (gitignored)
- `tests/` - Unit tests with pytest

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Orchestration | AutoGen (pyautogen) | Multi-agent coordination |
| Local LLMs | Ollama | Run quantized models (GGUF 4-bit) |
| API | FastAPI + Uvicorn | REST API server |
| Vector DB | ChromaDB | Memory/embeddings storage |
| Validation | Pydantic | Request/response schemas |
| Future UI | Streamlit | User interface |
| Testing | pytest + httpx | Unit and integration tests |
| Container | Docker + Docker Compose | Deployment |

## Agent Roles

| Agent | Role | Recommended Model |
|-------|------|-------------------|
| **Initiateur** | Launches initial reasoning | gemma:2b |
| **Créatif** | Generates original ideas | phi:latest |
| **Critique** | Analyzes and critiques responses | phi:latest |
| **Synthétiseur** | Merges best responses | gemma:2b |

## Development Setup

### Prerequisites
- Python 3.x
- pip3
- python3-venv
- git
- Docker + Docker Compose
- Ollama

### Quick Setup
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

The setup script will:
1. Verify and install system prerequisites
2. Install Ollama and download models (gemma:2b, phi)
3. Create a Python virtual environment at `../llm_env`
4. Install Python dependencies from requirements.txt

### Manual Setup
```bash
# Create and activate virtual environment
python3 -m venv llm_env
source llm_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Ensure Ollama is running with required models
ollama pull gemma:2b
ollama pull phi
```

### Running the API
```bash
source llm_env/bin/activate
cd api
uvicorn main:app --reload
```

API will be available at `http://localhost:8000`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/run_agent` | Send a message to the initiator agent |

### Request/Response Format
```python
# Request (AgentRequest)
{"message": "Your question here"}

# Response (AgentResponse)
{"response": "Agent's reply"}
```

## Code Conventions

### Python Style
- Use type hints with Pydantic for API schemas
- Logging via Python's `logging` module
- French comments and documentation preferred
- Follow FastAPI patterns for routing and dependency injection

### File Organization
- Routers in `api/routers/` with `router = APIRouter()`
- Schemas in `api/schemas/` using Pydantic BaseModel
- Entry point includes routers with prefix (`/api`)

### Imports Pattern
```python
# In main.py - relative imports from routers
from routers.agents import router as agent_router

# In routers - relative imports from schemas
from schemas.agent_schema import AgentRequest, AgentResponse
```

## Security Guidelines

- Never commit `.env` files or API keys
- Never expose LLM models directly to the internet
- Keep sensitive data out of version control
- Models, data, and environment files are gitignored

## Git Workflow

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make changes and commit with clear messages
4. Submit a Pull Request with documentation

### Gitignored Items
- Python cache (`__pycache__/`, `*.pyc`)
- Virtual environments (`llm_env/`, `venv/`, `env/`)
- IDE configs (`.vscode/`, `.idea/`)
- LLM models (`*.gguf`, `*.bin`, `*.pth`, `.ollama/`)
- Data directory (`data/`)
- Environment files (`*.env`)
- Build artifacts and logs

## Testing

```bash
# Run tests (when test files exist)
pytest tests/
```

Testing tools available: pytest, httpx (for FastAPI testing)

## Common Tasks for AI Assistants

### Adding a New Agent
1. Add agent configuration in `api/routers/agents.py`
2. Use AutoGen's `AssistantAgent` with Ollama config
3. Configure with appropriate model from Ollama

### Adding a New Endpoint
1. Add route in appropriate router (`api/routers/`)
2. Define request/response schemas in `api/schemas/`
3. Follow existing patterns for error handling and logging

### Modifying Agent Behavior
- Agent configs use Ollama's OpenAI-compatible API at `http://localhost:11434/v1`
- Models specified as `model_name:version` (e.g., `gemma:2b`, `phi:latest`)

## Hardware Requirements (Minimum)

- CPU: Ryzen 5 or equivalent
- GPU: NVIDIA GTX 1650 4GB+
- RAM: 16 GB (24 GB+ recommended)
- Storage: 512 GB SSD

## Current Project Status

This is an **early-stage experimental project**. Currently implemented:
- Basic FastAPI structure with one endpoint
- Single initiator agent connected to Ollama
- Setup script for environment configuration

Planned features:
- Multi-agent interaction with all 4 agent types
- ChromaDB integration for vector memory
- Streamlit UI
- Docker deployment
- Cloud scaling support (RunPod, RTX 4090, A100)

## Notes for Development

- The project uses Ollama's OpenAI-compatible endpoint (port 11434)
- Agent interactions have a 2-minute time limit (configurable)
- Exchanges use JSON format
- Virtual environment is created outside the project directory (`../llm_env`)

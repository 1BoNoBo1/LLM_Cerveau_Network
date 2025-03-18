# main.py
# import sys
import os

# Ajoutez le répertoire 'api' au sys.path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importez les modules FastAPI et routers.agents
from fastapi import FastAPI
from routers.agents import router as agent_router


# print("Current file path:", os.path.abspath(__file__))
# print("Parent directory path:", os.path.dirname(os.path.abspath(__file__)))
# print("Grandparent directory path:", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# print("sys.path:", sys.path)

app = FastAPI(
    title="API LLM Cerveau Network",
    description="API orchestre les interactions entre agents LLM via AutoGen",
    version="0.1"
)

app.include_router(agent_router, prefix="/api")

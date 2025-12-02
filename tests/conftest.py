# tests/conftest.py
# Configuration et fixtures pytest

import sys
import os
import tempfile
import pytest

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def temp_data_dir():
    """Crée un répertoire temporaire pour les tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def memoire_test(temp_data_dir):
    """Crée une instance de mémoire pour les tests."""
    from agents.memory import MemoireCerveau
    return MemoireCerveau(persist_directory=temp_data_dir)

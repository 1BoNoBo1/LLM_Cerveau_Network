# tests/test_memory.py
# Tests pour le module de mémoire ChromaDB

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMemoireCerveau:
    """Tests pour la classe MemoireCerveau."""

    def test_initialisation(self, memoire_test):
        """Test l'initialisation de la mémoire."""
        assert memoire_test is not None
        stats = memoire_test.stats()
        assert stats["nb_conversations"] == 0
        assert stats["nb_contextes"] == 0

    def test_sauvegarder_conversation(self, memoire_test):
        """Test la sauvegarde d'une conversation."""
        conv_id = memoire_test.sauvegarder(
            question="Quelle est la capitale de la France?",
            reponse="Paris est la capitale de la France.",
            mode="rapide"
        )

        assert conv_id is not None
        assert conv_id.startswith("conv_")

        stats = memoire_test.stats()
        assert stats["nb_conversations"] == 1

    def test_sauvegarder_plusieurs_conversations(self, memoire_test):
        """Test la sauvegarde de plusieurs conversations."""
        questions = [
            ("Qu'est-ce que Python?", "Python est un langage de programmation."),
            ("Qu'est-ce que JavaScript?", "JavaScript est un langage de script."),
            ("Qu'est-ce que Rust?", "Rust est un langage système."),
        ]

        for q, r in questions:
            memoire_test.sauvegarder(question=q, reponse=r)

        stats = memoire_test.stats()
        assert stats["nb_conversations"] == 3

    def test_rechercher_conversation(self, memoire_test):
        """Test la recherche de conversations."""
        # Sauvegarder des conversations
        memoire_test.sauvegarder(
            question="Comment cuisiner des pâtes?",
            reponse="Faire bouillir de l'eau, ajouter les pâtes..."
        )
        memoire_test.sauvegarder(
            question="Comment programmer en Python?",
            reponse="Installer Python, créer un fichier .py..."
        )

        # Rechercher
        resultats = memoire_test.rechercher("cuisine pâtes", k=5)

        assert len(resultats) > 0
        assert any("pâtes" in r["question"].lower() for r in resultats)

    def test_rechercher_vide(self, memoire_test):
        """Test la recherche avec une requête vide."""
        memoire_test.sauvegarder(
            question="Test question",
            reponse="Test réponse"
        )

        resultats = memoire_test.rechercher("", k=10)
        # Devrait retourner les plus récentes
        assert isinstance(resultats, list)

    def test_obtenir_contexte(self, memoire_test):
        """Test l'obtention du contexte pour les agents."""
        memoire_test.sauvegarder(
            question="Qu'est-ce que l'intelligence artificielle?",
            reponse="L'IA est un domaine de l'informatique..."
        )

        contexte = memoire_test.obtenir_contexte("IA et machine learning", k=3)

        assert isinstance(contexte, str)
        # Le contexte peut être vide si pas de résultats pertinents

    def test_ajouter_contexte_permanent(self, memoire_test):
        """Test l'ajout d'un contexte permanent."""
        memoire_test.ajouter_contexte(
            cle="info_utilisateur",
            valeur="L'utilisateur préfère les réponses courtes."
        )

        contextes = memoire_test.obtenir_tous_contextes()
        assert len(contextes) == 1
        assert contextes[0]["cle"] == "info_utilisateur"

    def test_stats(self, memoire_test):
        """Test les statistiques de la mémoire."""
        stats = memoire_test.stats()

        assert "nb_conversations" in stats
        assert "nb_contextes" in stats
        assert "persist_directory" in stats

    def test_effacer_sans_confirmation(self, memoire_test):
        """Test que l'effacement nécessite confirmation."""
        memoire_test.sauvegarder(question="Test", reponse="Test")

        # Sans confirmation, ne devrait pas effacer
        memoire_test.effacer(confirmer=False)

        stats = memoire_test.stats()
        assert stats["nb_conversations"] == 1

    def test_effacer_avec_confirmation(self, memoire_test):
        """Test l'effacement avec confirmation."""
        memoire_test.sauvegarder(question="Test", reponse="Test")

        memoire_test.effacer(confirmer=True)

        stats = memoire_test.stats()
        assert stats["nb_conversations"] == 0


class TestMetadataConversation:
    """Tests pour les métadonnées des conversations."""

    def test_metadata_mode(self, memoire_test):
        """Test que le mode est bien enregistré."""
        memoire_test.sauvegarder(
            question="Test",
            reponse="Réponse",
            mode="complet"
        )

        resultats = memoire_test.rechercher("Test", k=1)
        assert len(resultats) > 0
        assert resultats[0]["mode"] == "complet"

    def test_metadata_date(self, memoire_test):
        """Test que la date est bien enregistrée."""
        memoire_test.sauvegarder(
            question="Test date",
            reponse="Réponse avec date"
        )

        resultats = memoire_test.rechercher("Test date", k=1)
        assert len(resultats) > 0
        assert resultats[0]["date"] != ""

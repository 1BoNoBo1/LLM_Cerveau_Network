# agents/memory.py
# Mémoire persistante du Cerveau Network avec ChromaDB

import os
import logging
from datetime import datetime
from typing import Optional

import chromadb
from chromadb.config import Settings

from .config import OLLAMA_BASE_URL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Répertoire de stockage de la base vectorielle
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


class MemoireCerveau:
    """
    Mémoire à long terme du Cerveau Network.

    Utilise ChromaDB pour stocker et rechercher les conversations passées.
    Permet aux agents de se souvenir des échanges précédents.
    """

    def __init__(self, persist_directory: Optional[str] = None):
        """
        Initialise la mémoire du cerveau.

        Args:
            persist_directory: Répertoire de stockage (défaut: ./data/chromadb)
        """
        self.persist_dir = persist_directory or os.path.join(DATA_DIR, "chromadb")

        # Créer le répertoire si nécessaire
        os.makedirs(self.persist_dir, exist_ok=True)

        logger.info(f"Initialisation de la mémoire dans {self.persist_dir}")

        # Initialiser ChromaDB avec persistance
        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True,
            )
        )

        # Collection pour les conversations
        self.conversations = self.client.get_or_create_collection(
            name="conversations",
            metadata={"description": "Historique des conversations du Cerveau Network"}
        )

        # Collection pour les contextes (mémoire de travail)
        self.contextes = self.client.get_or_create_collection(
            name="contextes",
            metadata={"description": "Contextes et informations importantes"}
        )

        logger.info(f"Mémoire initialisée - {self.conversations.count()} conversations stockées")

    def sauvegarder(
        self,
        question: str,
        reponse: str,
        mode: str = "complet",
        metadata: Optional[dict] = None
    ) -> str:
        """
        Sauvegarde une conversation dans la mémoire.

        Args:
            question: La question posée
            reponse: La réponse générée
            mode: Mode de réflexion utilisé
            metadata: Métadonnées supplémentaires

        Returns:
            L'ID de la conversation sauvegardée
        """
        # Générer un ID unique
        conv_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

        # Préparer les métadonnées
        meta = {
            "date": datetime.now().isoformat(),
            "mode": mode,
            "question_length": len(question),
            "reponse_length": len(reponse),
        }
        if metadata:
            meta.update(metadata)

        # Créer le document à indexer (question + résumé de la réponse)
        document = f"Question: {question}\n\nRéponse: {reponse[:500]}"

        # Sauvegarder dans ChromaDB
        self.conversations.add(
            ids=[conv_id],
            documents=[document],
            metadatas=[meta],
        )

        logger.info(f"Conversation sauvegardée: {conv_id}")
        return conv_id

    def rechercher(
        self,
        requete: str,
        k: int = 5,
        filtre_mode: Optional[str] = None
    ) -> list[dict]:
        """
        Recherche des conversations similaires dans la mémoire.

        Args:
            requete: Texte de recherche
            k: Nombre de résultats à retourner
            filtre_mode: Filtrer par mode de réflexion

        Returns:
            Liste des conversations similaires
        """
        if not requete.strip():
            # Si requête vide, retourner les plus récentes
            resultats = self.conversations.get(
                limit=k,
                include=["documents", "metadatas"]
            )
        else:
            # Recherche par similarité
            where_filter = {"mode": filtre_mode} if filtre_mode else None

            resultats = self.conversations.query(
                query_texts=[requete],
                n_results=k,
                where=where_filter,
                include=["documents", "metadatas", "distances"]
            )

        # Formater les résultats
        conversations = []

        if "ids" in resultats and resultats["ids"]:
            ids = resultats["ids"][0] if isinstance(resultats["ids"][0], list) else resultats["ids"]
            docs = resultats["documents"][0] if isinstance(resultats["documents"][0], list) else resultats["documents"]
            metas = resultats["metadatas"][0] if isinstance(resultats["metadatas"][0], list) else resultats["metadatas"]

            for i, conv_id in enumerate(ids):
                doc = docs[i] if i < len(docs) else ""
                meta = metas[i] if i < len(metas) else {}

                # Parser le document pour extraire question et réponse
                parts = doc.split("\n\nRéponse: ")
                question = parts[0].replace("Question: ", "") if parts else ""
                reponse = parts[1] if len(parts) > 1 else ""

                conversations.append({
                    "id": conv_id,
                    "question": question,
                    "reponse": reponse,
                    "date": meta.get("date", ""),
                    "mode": meta.get("mode", ""),
                })

        return conversations

    def obtenir_contexte(self, question: str, k: int = 3) -> str:
        """
        Obtient le contexte pertinent pour une nouvelle question.

        Utilisé par les agents pour avoir accès aux conversations passées
        qui pourraient être utiles pour répondre à la question actuelle.

        Args:
            question: La nouvelle question
            k: Nombre de conversations à inclure dans le contexte

        Returns:
            Texte de contexte formaté pour les agents
        """
        conversations = self.rechercher(question, k=k)

        if not conversations:
            return ""

        contexte = "### Conversations passées pertinentes:\n\n"

        for i, conv in enumerate(conversations, 1):
            contexte += f"**Conversation {i}** ({conv.get('date', 'N/A')}):\n"
            contexte += f"- Question: {conv['question'][:200]}...\n" if len(conv['question']) > 200 else f"- Question: {conv['question']}\n"
            contexte += f"- Réponse: {conv['reponse'][:300]}...\n\n" if len(conv['reponse']) > 300 else f"- Réponse: {conv['reponse']}\n\n"

        return contexte

    def ajouter_contexte(self, cle: str, valeur: str, metadata: Optional[dict] = None):
        """
        Ajoute une information au contexte permanent.

        Utilisé pour stocker des informations importantes que les agents
        doivent toujours avoir en mémoire.

        Args:
            cle: Identifiant unique du contexte
            valeur: Contenu du contexte
            metadata: Métadonnées supplémentaires
        """
        meta = metadata or {}
        meta["date_ajout"] = datetime.now().isoformat()

        # Supprimer l'ancien si existe
        try:
            self.contextes.delete(ids=[cle])
        except Exception:
            pass

        self.contextes.add(
            ids=[cle],
            documents=[valeur],
            metadatas=[meta]
        )

        logger.info(f"Contexte ajouté: {cle}")

    def obtenir_tous_contextes(self) -> list[dict]:
        """Récupère tous les contextes permanents."""
        resultats = self.contextes.get(include=["documents", "metadatas"])

        contextes = []
        if resultats["ids"]:
            for i, cle in enumerate(resultats["ids"]):
                contextes.append({
                    "cle": cle,
                    "valeur": resultats["documents"][i],
                    "metadata": resultats["metadatas"][i]
                })

        return contextes

    def stats(self) -> dict:
        """Retourne les statistiques de la mémoire."""
        return {
            "nb_conversations": self.conversations.count(),
            "nb_contextes": self.contextes.count(),
            "persist_directory": self.persist_dir,
        }

    def effacer(self, confirmer: bool = False):
        """
        Efface toute la mémoire.

        Args:
            confirmer: Doit être True pour confirmer l'effacement
        """
        if not confirmer:
            logger.warning("Effacement annulé - confirmer=True requis")
            return

        self.client.delete_collection("conversations")
        self.client.delete_collection("contextes")

        # Recréer les collections vides
        self.conversations = self.client.create_collection(
            name="conversations",
            metadata={"description": "Historique des conversations du Cerveau Network"}
        )
        self.contextes = self.client.create_collection(
            name="contextes",
            metadata={"description": "Contextes et informations importantes"}
        )

        logger.info("Mémoire effacée")


# Instance globale
_memoire_instance = None


def get_memoire() -> MemoireCerveau:
    """Retourne l'instance globale de la mémoire (singleton)."""
    global _memoire_instance
    if _memoire_instance is None:
        _memoire_instance = MemoireCerveau()
    return _memoire_instance

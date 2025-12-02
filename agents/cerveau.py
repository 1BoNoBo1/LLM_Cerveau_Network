# agents/cerveau.py
# Cerveau Network - Orchestration des agents spécialisés avec CrewAI

import logging
from typing import Optional
from crewai import Agent, Task, Crew, Process, LLM

from .config import MODELES, OLLAMA_BASE_URL
from .memory import MemoireCerveau, get_memoire

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CerveauNetwork:
    """
    Cerveau collaboratif composé de 4 agents spécialisés :
    - Initiateur : Lance la réflexion initiale
    - Créatif : Génère des idées originales
    - Critique : Analyse et critique les réponses
    - Synthétiseur : Fusionne les meilleures réponses
    """

    def __init__(self, utiliser_memoire: bool = True):
        """
        Initialise les agents du cerveau.

        Args:
            utiliser_memoire: Active la mémoire ChromaDB pour le contexte
        """
        logger.info("Initialisation du Cerveau Network...")

        # Mémoire optionnelle
        self.memoire: Optional[MemoireCerveau] = None
        if utiliser_memoire:
            try:
                self.memoire = get_memoire()
                logger.info("Mémoire ChromaDB activée")
            except Exception as e:
                logger.warning(f"Mémoire non disponible: {e}")

        # Créer les LLMs pour chaque agent
        self.llm_initiateur = self._creer_llm(MODELES["initiateur"])
        self.llm_creatif = self._creer_llm(MODELES["creatif"])
        self.llm_critique = self._creer_llm(MODELES["critique"])
        self.llm_synthetiseur = self._creer_llm(MODELES["synthetiseur"])

        # Créer les agents
        self.initiateur = self._creer_initiateur()
        self.creatif = self._creer_creatif()
        self.critique = self._creer_critique()
        self.synthetiseur = self._creer_synthetiseur()

        logger.info("Cerveau Network initialisé avec succès")

    def _creer_llm(self, model_name: str) -> LLM:
        """Crée une instance LLM configurée pour Ollama."""
        return LLM(
            model=f"ollama/{model_name}",
            base_url=OLLAMA_BASE_URL,
        )

    def _creer_initiateur(self) -> Agent:
        """Crée l'agent Initiateur."""
        return Agent(
            role="Initiateur",
            goal="Analyser la question et lancer une réflexion structurée",
            backstory="""Tu es un penseur méthodique et analytique.
            Ton rôle est de recevoir une question ou un problème, de le décomposer
            en éléments clés, et de lancer une première réflexion structurée
            qui servira de base aux autres agents.""",
            llm=self.llm_initiateur,
            verbose=True,
            allow_delegation=False,
        )

    def _creer_creatif(self) -> Agent:
        """Crée l'agent Créatif."""
        return Agent(
            role="Créatif",
            goal="Proposer des idées originales et innovantes",
            backstory="""Tu es un esprit créatif et innovant.
            Tu penses différemment, tu explores des angles inattendus,
            et tu proposes des solutions originales que d'autres n'auraient pas envisagées.
            Tu n'as pas peur de suggérer des idées audacieuses.""",
            llm=self.llm_creatif,
            verbose=True,
            allow_delegation=False,
        )

    def _creer_critique(self) -> Agent:
        """Crée l'agent Critique."""
        return Agent(
            role="Critique",
            goal="Analyser objectivement les forces et faiblesses des propositions",
            backstory="""Tu es un analyste rigoureux et objectif.
            Tu examines les idées avec un oeil critique mais constructif.
            Tu identifies les points forts à conserver et les faiblesses à améliorer.
            Tu poses les bonnes questions et anticipes les problèmes potentiels.""",
            llm=self.llm_critique,
            verbose=True,
            allow_delegation=False,
        )

    def _creer_synthetiseur(self) -> Agent:
        """Crée l'agent Synthétiseur."""
        return Agent(
            role="Synthétiseur",
            goal="Créer une réponse finale cohérente et complète",
            backstory="""Tu es un médiateur et un intégrateur.
            Tu prends les meilleures éléments de chaque contribution,
            tu résous les contradictions, et tu crées une synthèse harmonieuse
            qui répond de manière complète et équilibrée à la question initiale.""",
            llm=self.llm_synthetiseur,
            verbose=True,
            allow_delegation=False,
        )

    def _obtenir_contexte(self, question: str) -> str:
        """Récupère le contexte pertinent de la mémoire."""
        if not self.memoire:
            return ""

        try:
            return self.memoire.obtenir_contexte(question, k=3)
        except Exception as e:
            logger.warning(f"Erreur récupération contexte: {e}")
            return ""

    def _sauvegarder_conversation(self, question: str, reponse: str, mode: str):
        """Sauvegarde la conversation dans la mémoire."""
        if not self.memoire:
            return

        try:
            self.memoire.sauvegarder(question, reponse, mode)
        except Exception as e:
            logger.warning(f"Erreur sauvegarde mémoire: {e}")

    def penser(self, question: str, sauvegarder: bool = True) -> dict:
        """
        Lance le processus de réflexion collaborative sur une question.

        Args:
            question: La question ou le problème à analyser
            sauvegarder: Sauvegarder dans la mémoire (défaut: True)

        Returns:
            dict avec les contributions de chaque agent et la synthèse finale
        """
        logger.info(f"Nouvelle réflexion sur : {question[:50]}...")

        # Récupérer le contexte des conversations passées
        contexte = self._obtenir_contexte(question)
        contexte_str = f"\n\n{contexte}" if contexte else ""

        # Définir les tâches pour chaque agent
        tache_initiale = Task(
            description=f"""Analyse cette question et fournis une réflexion initiale structurée :

            Question : {question}
            {contexte_str}

            Tu dois :
            1. Identifier les éléments clés de la question
            2. Reformuler le problème si nécessaire
            3. Proposer les axes de réflexion principaux""",
            expected_output="Une analyse structurée avec les points clés et axes de réflexion",
            agent=self.initiateur,
        )

        tache_creative = Task(
            description="""En te basant sur l'analyse initiale, propose des idées créatives.

            Tu dois :
            1. Proposer 2-3 idées originales ou angles nouveaux
            2. Explorer des solutions non conventionnelles
            3. Penser au-delà des évidences""",
            expected_output="2-3 idées créatives avec explications",
            agent=self.creatif,
        )

        tache_critique = Task(
            description="""Analyse de manière critique les propositions précédentes.

            Tu dois :
            1. Identifier les forces de chaque idée
            2. Pointer les faiblesses ou risques
            3. Suggérer des améliorations concrètes""",
            expected_output="Analyse critique constructive avec forces, faiblesses et améliorations",
            agent=self.critique,
        )

        tache_synthese = Task(
            description=f"""Crée une synthèse finale qui répond à la question originale.

            Question originale : {question}

            Tu dois :
            1. Intégrer les meilleures idées
            2. Tenir compte des critiques
            3. Fournir une réponse complète et cohérente""",
            expected_output="Réponse finale synthétique et complète",
            agent=self.synthetiseur,
        )

        # Créer et lancer le crew
        crew = Crew(
            agents=[self.initiateur, self.creatif, self.critique, self.synthetiseur],
            tasks=[tache_initiale, tache_creative, tache_critique, tache_synthese],
            process=Process.sequential,
            verbose=True,
        )

        # Exécuter la réflexion
        resultat = crew.kickoff()
        synthese = str(resultat)

        # Sauvegarder dans la mémoire
        if sauvegarder:
            self._sauvegarder_conversation(question, synthese, "complet")

        logger.info("Réflexion terminée avec succès")

        return {
            "question": question,
            "synthese": synthese,
            "succes": True,
            "contexte_utilise": bool(contexte),
        }

    def penser_rapide(self, question: str, sauvegarder: bool = True) -> dict:
        """
        Version simplifiée avec seulement Initiateur + Synthétiseur.
        Plus rapide mais moins approfondie.

        Args:
            question: La question à analyser
            sauvegarder: Sauvegarder dans la mémoire (défaut: True)

        Returns:
            dict avec la réponse
        """
        logger.info(f"Réflexion rapide sur : {question[:50]}...")

        # Récupérer le contexte
        contexte = self._obtenir_contexte(question)
        contexte_str = f"\n\nContexte des conversations passées:\n{contexte}" if contexte else ""

        tache_initiale = Task(
            description=f"""Analyse cette question et fournis une réponse structurée :

            Question : {question}
            {contexte_str}""",
            expected_output="Analyse et réponse structurée",
            agent=self.initiateur,
        )

        tache_synthese = Task(
            description="Améliore et finalise la réponse précédente.",
            expected_output="Réponse finale améliorée",
            agent=self.synthetiseur,
        )

        crew = Crew(
            agents=[self.initiateur, self.synthetiseur],
            tasks=[tache_initiale, tache_synthese],
            process=Process.sequential,
            verbose=True,
        )

        resultat = crew.kickoff()
        synthese = str(resultat)

        # Sauvegarder dans la mémoire
        if sauvegarder:
            self._sauvegarder_conversation(question, synthese, "rapide")

        return {
            "question": question,
            "synthese": synthese,
            "succes": True,
            "contexte_utilise": bool(contexte),
        }

    def stats_memoire(self) -> dict:
        """Retourne les statistiques de la mémoire."""
        if not self.memoire:
            return {"memoire_active": False}

        stats = self.memoire.stats()
        stats["memoire_active"] = True
        return stats


# Instance globale pour réutilisation
_cerveau_instance = None


def get_cerveau() -> CerveauNetwork:
    """Retourne l'instance globale du Cerveau Network (singleton)."""
    global _cerveau_instance
    if _cerveau_instance is None:
        _cerveau_instance = CerveauNetwork()
    return _cerveau_instance

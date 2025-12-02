# agents/cerveau.py
# Cerveau Network - Orchestration des agents spécialisés avec CrewAI

import logging
from crewai import Agent, Task, Crew, Process, LLM

from .config import MODELES, OLLAMA_BASE_URL

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

    def __init__(self):
        """Initialise les agents du cerveau."""
        logger.info("Initialisation du Cerveau Network...")

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

    def penser(self, question: str) -> dict:
        """
        Lance le processus de réflexion collaborative sur une question.

        Args:
            question: La question ou le problème à analyser

        Returns:
            dict avec les contributions de chaque agent et la synthèse finale
        """
        logger.info(f"Nouvelle réflexion sur : {question[:50]}...")

        # Définir les tâches pour chaque agent
        tache_initiale = Task(
            description=f"""Analyse cette question et fournis une réflexion initiale structurée :

            Question : {question}

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
            process=Process.sequential,  # Exécution séquentielle
            verbose=True,
        )

        # Exécuter la réflexion
        resultat = crew.kickoff()

        logger.info("Réflexion terminée avec succès")

        return {
            "question": question,
            "synthese": str(resultat),
            "succes": True,
        }

    def penser_rapide(self, question: str) -> dict:
        """
        Version simplifiée avec seulement Initiateur + Synthétiseur.
        Plus rapide mais moins approfondie.

        Args:
            question: La question à analyser

        Returns:
            dict avec la réponse
        """
        logger.info(f"Réflexion rapide sur : {question[:50]}...")

        tache_initiale = Task(
            description=f"""Analyse cette question et fournis une réponse structurée :

            Question : {question}""",
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

        return {
            "question": question,
            "synthese": str(resultat),
            "succes": True,
        }


# Instance globale pour réutilisation
_cerveau_instance = None


def get_cerveau() -> CerveauNetwork:
    """Retourne l'instance globale du Cerveau Network (singleton)."""
    global _cerveau_instance
    if _cerveau_instance is None:
        _cerveau_instance = CerveauNetwork()
    return _cerveau_instance

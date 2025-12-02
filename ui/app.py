# ui/app.py
# Interface Streamlit pour LLM Cerveau Network

import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from datetime import datetime

from agents.cerveau import get_cerveau
from agents.memory import MemoireCerveau

# Configuration de la page
st.set_page_config(
    page_title="LLM Cerveau Network",
    page_icon="🧠",
    layout="wide",
)

# CSS personnalisé
st.markdown("""
<style>
    .agent-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .initiateur { background-color: #e3f2fd; }
    .creatif { background-color: #f3e5f5; }
    .critique { background-color: #fff3e0; }
    .synthetiseur { background-color: #e8f5e9; }
    .stSpinner > div { text-align: center; }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """Initialise les variables de session."""
    if "historique" not in st.session_state:
        st.session_state.historique = []
    if "memoire" not in st.session_state:
        st.session_state.memoire = MemoireCerveau()
    if "cerveau" not in st.session_state:
        st.session_state.cerveau = None


def afficher_historique():
    """Affiche l'historique des conversations."""
    for item in st.session_state.historique:
        with st.container():
            st.markdown(f"**🗣️ Question** ({item['timestamp']})")
            st.info(item["question"])
            st.markdown(f"**🧠 Réponse** (mode: {item['mode']})")
            st.success(item["reponse"])
            st.divider()


def main():
    """Point d'entrée de l'application Streamlit."""
    init_session_state()

    # En-tête
    st.title("🧠 LLM Cerveau Network")
    st.markdown("*Un cerveau collaboratif composé de 4 agents spécialisés*")

    # Sidebar - Configuration et informations
    with st.sidebar:
        st.header("⚙️ Configuration")

        mode = st.radio(
            "Mode de réflexion",
            options=["complet", "rapide"],
            index=0,
            help="Complet: 4 agents | Rapide: 2 agents"
        )

        st.divider()

        st.header("🤖 Les Agents")
        st.markdown("""
        - **Initiateur** : Analyse le problème
        - **Créatif** : Propose des idées
        - **Critique** : Évalue les propositions
        - **Synthétiseur** : Crée la réponse finale
        """)

        st.divider()

        st.header("💾 Mémoire")
        nb_souvenirs = len(st.session_state.memoire.rechercher("", k=100)) if st.session_state.memoire else 0
        st.metric("Conversations mémorisées", nb_souvenirs)

        if st.button("🗑️ Effacer l'historique"):
            st.session_state.historique = []
            st.rerun()

    # Zone principale
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("💬 Nouvelle Question")

        question = st.text_area(
            "Posez votre question au cerveau",
            height=100,
            placeholder="Exemple: Comment améliorer ma productivité au travail?",
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            lancer = st.button("🚀 Lancer la réflexion", type="primary", use_container_width=True)

        with col_btn2:
            rechercher_memoire = st.button("🔍 Chercher dans la mémoire", use_container_width=True)

        # Lancer la réflexion
        if lancer and question:
            with st.spinner("🧠 Les agents réfléchissent..."):
                try:
                    # Initialiser le cerveau si nécessaire
                    if st.session_state.cerveau is None:
                        st.session_state.cerveau = get_cerveau()

                    # Lancer la réflexion
                    if mode == "rapide":
                        resultat = st.session_state.cerveau.penser_rapide(question)
                    else:
                        resultat = st.session_state.cerveau.penser(question)

                    # Sauvegarder dans la mémoire
                    st.session_state.memoire.sauvegarder(
                        question=question,
                        reponse=resultat["synthese"],
                        mode=mode,
                    )

                    # Ajouter à l'historique de session
                    st.session_state.historique.append({
                        "question": question,
                        "reponse": resultat["synthese"],
                        "mode": mode,
                        "timestamp": datetime.now().strftime("%H:%M:%S"),
                    })

                    # Afficher le résultat
                    st.success("✅ Réflexion terminée!")
                    st.markdown("### 📝 Synthèse")
                    st.write(resultat["synthese"])

                except Exception as e:
                    st.error(f"❌ Erreur: {str(e)}")
                    st.info("💡 Vérifiez qu'Ollama est lancé avec le modèle qwen2.5:3b")

        # Rechercher dans la mémoire
        if rechercher_memoire and question:
            with st.spinner("🔍 Recherche en cours..."):
                resultats = st.session_state.memoire.rechercher(question, k=3)

                if resultats:
                    st.markdown("### 💾 Conversations similaires trouvées")
                    for i, r in enumerate(resultats, 1):
                        with st.expander(f"Résultat {i} - {r.get('date', 'N/A')}"):
                            st.markdown(f"**Question:** {r['question']}")
                            st.markdown(f"**Réponse:** {r['reponse']}")
                else:
                    st.info("Aucune conversation similaire trouvée.")

    with col2:
        st.header("📜 Historique de session")

        if st.session_state.historique:
            for i, item in enumerate(reversed(st.session_state.historique[-5:])):
                with st.expander(f"💭 {item['question'][:30]}...", expanded=(i == 0)):
                    st.markdown(f"*Mode: {item['mode']} | {item['timestamp']}*")
                    st.write(item["reponse"][:200] + "..." if len(item["reponse"]) > 200 else item["reponse"])
        else:
            st.info("Aucune conversation dans cette session.")


if __name__ == "__main__":
    main()

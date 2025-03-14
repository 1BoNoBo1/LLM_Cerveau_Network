# 🧠 LLM Cerveau Network

**Un cerveau collaboratif composé d'agents spécialisés utilisant plusieurs modèles LLM quantifiés, échangeant et raisonnant ensemble via AutoGen et Ollama.**

---

## 🚀 Objectif du projet

Ce projet expérimental vise à créer une **intelligence artificielle distribuée** où chaque modèle de langage (LLM) joue le rôle d'un neurone spécialisé. Les modèles communiquent entre eux afin de générer collectivement des réponses cohérentes et intelligentes sur divers sujets, avec une latence optimisée pour être utilisable sur des machines modestes (ex: PC portable GTX 1650 4GB).

---

## ⚙️ Architecture technique
- **Orchestrateur** : [AutoGen](https://github.com/microsoft/autogen)
- **Modèles locaux** : Ollama (modèles quantifiés GGUF 4-bit)
- **API REST** : FastAPI
- **Mémoire vectorielle** : ChromaDB
- **Interface utilisateur (future)** : Streamlit
- **Conteneurisation** : Docker et Docker Compose
- **Développement** : Ubuntu + VSCode

---

## 📌 Spécifications matérielles minimales
- **CPU** : Ryzen 5 (ou similaire)
- **GPU** : NVIDIA GTX 1650 4GB (ou supérieure)
- **RAM** : 16 Go (idéalement 24 Go ou plus)
- **Stockage** : SSD 512 Go minimum

---

## 🚀 Installation rapide

Clonez le dépôt et installez les dépendances :

```bash
git clone https://github.com/1BoNoBo1/LLM-Cerveau-Network.git
cd LLM-Cerveau-Network
chmod +x scripts/setup.sh
./scripts/setup.sh
```

---

## 🧩 Rôles des Agents (neurones LLM)

| Agent            | Rôle                          | Modèle recommandé (GTX 1650) |
|------------------|--------------------------------------|-----------------------------|
| **Initiateur**   | Lance la réflexion initiale  | Gemma 2B (quantifié) |
| **Créatif**      | Génère des idées originales | Phi-2 (quantifié) |
| **Critique**     | Analyse et critique les réponses | Phi-2 (quantifié) |
| **Synthétiseur** | Fusionne les meilleures réponses | Gemma 2B (quantifié) |

---

## 🔄 Protocole d’interaction entre agents
- L’utilisateur déclenche une session via l’API FastAPI.
- Les agents interagissent séquentiellement avec une limite de temps initiale de **2 minutes** (ajustable).
- Les échanges sont structurés en JSON (format modulable).

---

## 📁 Structure du dépôt
```
LLM-Cerveau-Network/
├── agents/              # Agents spécialisés
├── api/                 # API FastAPI
├── docker/              # Fichiers Docker
├── models/              # Stockage des modèles LLM quantifiés
├── data/                # Base de données vectorielle
├── scripts/             # Scripts setup et lancement rapide
├── tests/               # Tests unitaires
├── .gitignore
├── requirements.txt     # Dépendances Python
└── README.md            # Documentation
```

---

## 🚀 Évolutions prévues
- Intégration interface Streamlit
- Optimisation pour utilisation GPU/Cloud (RunPod, RTX 4090, A100)
- Ajout d'agents multimodaux

---

## 📖 Contribution
Toute contribution est bienvenue ! Suivez ces étapes :
1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b fonctionnalité`)
3. Proposez une Pull Request claire et documentée

---

## ⚠️ Sécurité et confidentialité
- Aucun modèle n'est exposé directement sur internet.
- Les clés API ou informations sensibles ne doivent jamais être versionnées.

---

## 📚 Licence
Ce projet est sous licence MIT. Libre d'être partagé, modifié, utilisé pour l’éducation et la communauté.


#!/bin/bash
# setup.sh - Setup script for LLM_Cerveau_Network project
# Generated based on LLM_Cerveau_Network/README.md

# Couleurs pour sortie terminal
VERT='\033[0;32m'
ROUGE='\033[0;31m'
BLEU='\033[0;34m'
JAUNE='\033[0;33m'
NC='\033[0m' # Pas de couleur

# Display banner
echo "================================================"
echo "           LLM_Cerveau_Network Setup"
echo "================================================"

# |||||||||||||||||||||||||||||||||--- Fonction du Script ---|||||||||||||||||||||||||||||||

# Fonction pour vérifier si une commande existe
commande_existe() {
        command -v "$1" >/dev/null 2>&1
}

# Fonction pour vérifier si un package est installé
package_existe() {
        dpkg -s "$1" &>/dev/null
}

# Fonction pour afficher les messages d'étape
etape() {
        echo -e "${BLEU}\\n===> $1${NC}\\n"
}

# Fonction pour afficher les messages de succès
succes() {
        echo -e "${VERT}[✓] $1${NC}"
}

# Fonction pour afficher les messages d'avertissement
avertissement() {
        echo -e "${JAUNE}[!] $1${NC}"
}

# Fonction pour afficher les messages d'erreur
erreur() {
        echo -e "${ROUGE}[✗] $1${NC}"
}

# Fonction pour installer un package avec confirmation
installer_package() {
        local package=$1
        local cmd=$2
        
        echo -e "${JAUNE}$package n'est pas installé.${NC}"
        read -p "Voulez-vous l'installer maintenant? (o/n): " reponse
        
        if [[ $reponse == "o" || $reponse == "O" || $reponse == "oui" ]]; then
                echo "Installation de $package en cours..."
                eval $cmd || { erreur "L'installation de $package a échoué."; return 1; }
                succes "$package a été installé avec succès!"
                return 0
        else
                avertissement "Installation de $package ignorée. Certaines fonctionnalités pourraient ne pas être disponibles."
                return 1
        fi
}

# |||||||||||||||||||||||||||||||||--- Vérification ---|||||||||||||||||||||||||||||||
# Vérification et installation des prérequis
etape "Vérification des prérequis système"

# Vérification du système d'exploitation
if [ -f /etc/lsb-release ]; then
    # Système basé sur Debian ou Ubuntu
    OS="debian"
elif [ -f /etc/redhat-release ]; then
    # Système basé sur Red Hat ou CentOS
    OS="redhat"
else
    erreur "Système d'exploitation non supporté."
    exit 1
fi


# Vérifier si Python est installé
if commande_existe python3; then
        PYTHON_VERSION=$(python3 --version 2>&1 | cut -d ' ' -f 2)
        succes "Python installé (version $PYTHON_VERSION)"
else
        erreur "Python 3 n'est pas installé."
        if installer_package "Python 3" "sudo apt-get update && sudo apt-get install -y python3"; then
                PYTHON_VERSION=$(python3 --version 2>&1 | cut -d ' ' -f 2)
                succes "Python installé (version $PYTHON_VERSION)"
        else
                erreur "Python 3 est requis pour continuer. Installation abandonnée."
                exit 1
        fi
fi

# Vérifier si pip est installé
if commande_existe pip3; then
        succes "pip installé"
else
        erreur "pip n'est pas installé."
        if installer_package "pip3" "sudo apt-get install -y python3-pip"; then
                succes "pip installé"
        else
                erreur "pip3 est requis pour continuer. Installation abandonnée."
                exit 1
        fi
fi

# vérifier si python3-venv est installé
if package_existe python3-venv; then
        succes "python3-venv installé"
else
        erreur "python3-venv n'est pas installé."
        if installer_package "python3-venv" "sudo apt-get install -y python3-venv"; then
                succes "python3-venv installé"
        else
                erreur "python3-venv est requis pour continuer. Installation abandonnée."
                exit 1
        fi
fi

# Vérifier si git est installé
if commande_existe git; then
        succes "git installé"
else
        erreur "git n'est pas installé."
        if installer_package "git" "sudo apt-get install -y git"; then
                succes "git installé"
        else
                erreur "git est requis pour continuer. Installation abandonnée."
                exit 1
        fi
fi

# vérifier si docker est installé
if commande_existe docker; then
        succes "docker installé"
else
        erreur "docker n'est pas installé."
        if installer_package "docker" "sudo apt-get install -y docker"; then
                succes "docker installé"
        else
                erreur "docker est requis pour continuer. Installation abandonnée."
                exit 1
        fi
fi

# vérifier si docker-compose est installé
if commande_existe docker-compose; then
        succes "docker-compose installé"
else
        erreur "docker-compose n'est pas installé."
        if installer_package "docker-compose" "sudo apt-get install -y docker-compose"; then
                succes "docker-compose installé"
        else
                erreur "docker-compose est requis pour continuer. Installation abandonnée."
                exit 1
        fi
fi

# Vérifier que le service Docker est actif
if systemctl is-active --quiet docker; then
    succes "Le service Docker est actif."
else
    erreur "Le service Docker n'est pas actif. Tentative de démarrage..."
    if sudo systemctl start docker; then
        succes "Le service Docker a démarré."
    else
        erreur "Impossible de démarrer Docker. Installation abandonnée."
        exit 1
    fi
fi

# Vérifier que l'utilisateur courant appartient au groupe docker
if groups "$USER" | grep -q "\bdocker\b"; then
    succes "L'utilisateur '$USER' appartient au groupe docker."
else
    erreur "L'utilisateur '$USER' n'appartient pas au groupe docker. Ajout en cours..."
    if sudo usermod -aG docker "$USER"; then
        succes "Ajout de '$USER' au groupe docker réussi. Veuillez vous déconnecter/reconnecter pour appliquer les changements."
    else
        erreur "Échec de l'ajout de l'utilisateur au groupe docker."
    fi
fi

# |||||||||||||||||||||||||||||||||--- Installation ollama ---|||||||||||||||||||||||||||||||
etape "Installation d'Ollama (Gestionnaire des modèles LLM quantifiés)"
if commande_existe ollama; then
    succes "Ollama déjà installé"
else
    curl -fsSL https://ollama.com/install.sh | sh
    if commande_existe ollama; then
        succes "Ollama installé avec succès"
    else
        erreur "Échec installation Ollama"
        exit 1
    fi
fi

telecharger_modele() {
    local modele=$1
    local version=$2
    etape "Téléchargement du modèle $modele $version"
    if commande_existe ollama; then
        if ollama list | grep -q "$modele:$version"; then
            succes "Modèle $modele $version déjà présent"
        else
            if ollama pull $modele:$version; then
                succes "Modèle $modele $version téléchargé avec succès"
            else
                erreur "Échec du téléchargement du modèle $modele $version"
            fi
        fi
    else
        erreur "Ollama n'est pas installé. Impossible de télécharger le modèle $modele $version"
        exit 1
    fi
}

telecharger_modele "gemma" "2b"
telecharger_modele "phi"




etape "Tous les prérequis sont satisfaits. Prêt à continuer l'installation!"


# |||||||||||||||||||||||||||||||||--- Environnement Python ---|||||||||||||||||||||||||||||||
etape "Création et configuration de l'environnement Python virtuel"

# Définir le chemin du virtualenv
VENV_DIR="$(pwd)/../llm_env"

# Vérifier si l'environnement virtuel existe déjà
if [ -d "$VENV_DIR" ]; then
    avertissement "L'environnement virtuel existe déjà à $VENV_DIR"
    read -p "Voulez-vous le recréer ? (o/n): " recreer_venv
    if [[ "$recreer_venv" == "o" || "$recreer_venv" == "O" || "$recreer_venv" == "oui" ]]; then
        rm -rf "$VENV_DIR"
        succes "Ancien environnement virtuel supprimé."
        python3 -m venv "$VENV_DIR"
        succes "Nouvel environnement virtuel créé avec succès à $VENV_DIR."
    else
        succes "Utilisation de l'environnement virtuel existant."
    fi
else
    python3 -m venv "$VENV_DIR"
    succes "Environnement virtuel créé avec succès à $VENV_DIR."
fi

# Activer l'environnement virtuel et installer les dépendances
etape "Installation des dépendances Python"
source "$VENV_DIR/bin/activate"
etape "Mise à jour de pip"
pip install --upgrade pip
if [ $? -eq 0 ]; then
        succes " mis à jour avec succès"
else
        erreur "Échec de la mise à jour de pip"
        exit 1
fi

# Vérifier si le fichier requirements.txt existe
if [ -f "../requirements.txt" ]; then
        pip install -r "../requirements.txt"
        if [ $? -eq 0 ]; then
                succes "Dépendances Python installées avec succès"
        else
                erreur "Échec de l'installation des dépendances Python"
                exit 1
        fi
else
        avertissement "Fichier requirements.txt non trouvé. Aucune dépendance à installer."
fi

# lister les packages installés
etape "Liste des packages installés"
pip list

# Désactiver l'environnement virtuel
deactivate
succes "Environnement Python configuré et prêt à l'emploi"

etape "Instructions d'utilisation:"
echo -e "Pour activer l'environnement virtuel qui est $VENV_DIR: ${VERT}source llm_env/bin/activate${NC}"
echo -e "Pour quitter l'environnement virtuel: ${VERT}deactivate${NC}"
exit 0
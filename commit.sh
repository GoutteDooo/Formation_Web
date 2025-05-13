#!/bin/bash
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Initialisation de la variable booléenne
no_changes=false

while true; do
    # Vérifier s'il y a des fichiers modifiés ou en attente d'ajout
    if [[ -n $(git status --porcelain) ]]; then
        echo -e "${RED}🚀 Des modifications détectées, commit en cours...${NC}"


        # Ajouter les fichiers modifiés
        git aa

        # Commiter avec la date actuelle
        ./git_datecommit.sh

        # Réinitialiser la variable car un commit a été fait
        no_changes=false

        echo -e "${GREEN}✅ Commit effectué à $(date '+%Y-%m-%d %H:%M:%S')${NC}"
        echo -e "\a"  # Émet un bip sonore sur certains terminaux
    else
        echo -e "${YELLOW}😴 Aucune modification détectée, en attente...${NC}"
        
        # Si aucun changement n'a été détecté, on active le mode rapide (30s)
        if [ "$no_changes" = false ]; then
            no_changes=true
            echo "⏳ Passage au mode d'attente rapide (30 secondes)"
        fi
    fi

    # Définition du temps de pause en fonction de la variable `no_changes`
    if [ "$no_changes" = true ]; then
        sleep 30  # Mode rapide
    else
        sleep 180  # Mode normal
    fi
done

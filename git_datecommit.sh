#!/bin/bash

# Générer la date du jour
commit_message="$(date '+%Y-%m-%d %H:%M:%S')"

# Ajouter tous les fichiers modifiés
git add .

# Faire le commit avec la date
git commit -m "$commit_message"
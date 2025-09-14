#!/bin/bash

# Script pour pousser sélectivement vers la branche release

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Préparation du push vers la branche release...${NC}"

# Vérifier qu'on est dans un repo git
if [ ! -d ".git" ]; then
    echo -e "${RED}Erreur: Ce n'est pas un dépôt git${NC}"
    exit 1
fi

# Sauvegarder la branche actuelle
CURRENT_BRANCH=$(git branch --show-current)
echo -e "${YELLOW}Branche actuelle: ${CURRENT_BRANCH}${NC}"

# Créer ou basculer vers la branche release
if git show-ref --verify --quiet refs/heads/release; then
    echo -e "${YELLOW}Basculement vers la branche release existante${NC}"
    git checkout release
else
    echo -e "${YELLOW}Création de la branche release${NC}"
    git checkout --orphan release
    git rm -rf . 2>/dev/null || true
fi

# Revenir temporairement sur la branche principale pour récupérer les fichiers
git checkout $CURRENT_BRANCH

# Liste des fichiers et dossiers à inclure
FILES_TO_INCLUDE=(
    "source"
    "docs"
    ".gitignore"
    "README.md"
    "deploy.sh"
    "requirements-test.txt"
    "start.sh"
)

# Vérifier que les fichiers/dossiers existent
MISSING_FILES=()
for item in "${FILES_TO_INCLUDE[@]}"; do
    if [ ! -e "$item" ]; then
        MISSING_FILES+=("$item")
    fi
done

if [ ${#MISSING_FILES[@]} -gt 0 ]; then
    echo -e "${RED}Attention: Les fichiers/dossiers suivants n'existent pas:${NC}"
    for missing in "${MISSING_FILES[@]}"; do
        echo -e "${RED}  - $missing${NC}"
    done
    read -p "Continuer quand même? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Opération annulée${NC}"
        exit 1
    fi
fi

# Retourner sur la branche release
git checkout release

# Nettoyer la branche release
git rm -rf . 2>/dev/null || true

# Copier les fichiers depuis la branche principale
for item in "${FILES_TO_INCLUDE[@]}"; do
    if [ -e "../$item" ] || git show $CURRENT_BRANCH:$item >/dev/null 2>&1; then
        echo -e "${GREEN}Ajout de: $item${NC}"
        git checkout $CURRENT_BRANCH -- $item 2>/dev/null || echo -e "${YELLOW}  Fichier $item non trouvé, ignoré${NC}"
    fi
done

# Ajouter tous les fichiers
git add .

# Commit si il y a des changements
if ! git diff --cached --quiet; then
    COMMIT_MSG="Release: $(date '+%Y-%m-%d %H:%M:%S')"
    git commit -m "$COMMIT_MSG"
    echo -e "${GREEN}Commit créé: $COMMIT_MSG${NC}"
    
    # Pousser vers origin
    echo -e "${YELLOW}Push vers origin/release...${NC}"
    git push origin release
    echo -e "${GREEN}Push terminé avec succès!${NC}"
else
    echo -e "${YELLOW}Aucun changement à commiter${NC}"
fi

# Retourner sur la branche originale
git checkout $CURRENT_BRANCH
echo -e "${GREEN}Retour sur la branche: $CURRENT_BRANCH${NC}"

echo -e "${GREEN}Script terminé!${NC}"

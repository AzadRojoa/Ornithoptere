#!/bin/bash

# Configuration
SOURCE_DIR="./source"
KEEP_FILE="boot.py"
TMP_MPSH=$(mktemp)
PORTS=( $(ls /dev/ttyUSB*) )

# 1. Choix du type de programme
echo "Quel programme voulez-vous envoyer ?"
select PROGRAM in "emission" "reception"; do
    case $PROGRAM in
        emission ) MAIN_FILE="programme_antenne_emission.py"; break;;
        reception ) MAIN_FILE="programme_antenne_reception.py"; break;;
        * ) echo "Choix invalide";;
    esac
done

# 2. Choisir les ports (si 2 ESP connectées)
if [[ ${#PORTS[@]} -eq 2 ]]; then
    echo "Deux ESP détectées :"
    echo "1) ${PORTS[0]}"
    echo "2) ${PORTS[1]}"
    echo "Quel port est pour le programme '$PROGRAM' ? (1 ou 2)"
    read -r CHOICE
    if [[ $CHOICE == 1 ]]; then
        TARGET_PORT=${PORTS[0]}
    else
        TARGET_PORT=${PORTS[1]}
    fi
elif [[ ${#PORTS[@]} -eq 1 ]]; then
    TARGET_PORT=${PORTS[0]}
else
    echo "Aucune ESP détectée sur /dev/ttyUSB*"
    exit 1
fi

echo "→ Déploiement sur $TARGET_PORT"

# 3. Lister les fichiers existants sur l’ESP
echo "open $TARGET_PORT" > "$TMP_MPSH"
echo "ls" >> "$TMP_MPSH"
echo "exit" >> "$TMP_MPSH"

FILES=$(mpfshell -n -f "$TMP_MPSH" | grep -E '^\s+\S' | awk '{print $1}' | grep -v "$KEEP_FILE")

# 4. Générer le script MPFSHELL pour effacer et uploader
> "$TMP_MPSH"
echo "open $TARGET_PORT" >> "$TMP_MPSH"

# Supprimer tous les fichiers sauf boot.py
for file in $FILES; do
    echo "rm $file" >> "$TMP_MPSH"
done

# Uploader tous les fichiers, en renommant le bon programme en main.py
for filepath in "$SOURCE_DIR"/*; do
    filename=$(basename "$filepath")
    if [[ "$filename" == "$MAIN_FILE" ]]; then
        echo "put $filepath main.py" >> "$TMP_MPSH"
    else
        echo "put $filepath $filename" >> "$TMP_MPSH"
    fi
done

echo "exit" >> "$TMP_MPSH"

# 5. Exécuter le script
mpfshell -n -f "$TMP_MPSH"

# 6. Nettoyage
rm "$TMP_MPSH"

echo "✅ Déploiement terminé sur $TARGET_PORT"

#!/bin/bash

# Configuration
SOURCE_DIR="./source"
KEEP_FILE="boot.py"
TMP_MPSH=$(mktemp)
PORTS=( $(ls /dev/ttyUSB*) )

# 1. Choix du type de programme
echo "Quel programme voulez-vous envoyer ?"
select PROGRAM in "emetteur" "recepteur"; do
    case $PROGRAM in
        emetteur ) MAIN_FILE="emetteur_esp32.py"; break;;
        recepteur ) MAIN_FILE="recepteur_esp32.py"; break;;
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

# Liste des fichiers essentiels à déployer (exclure simulation)
ESSENTIAL_FILES=(
    "programme_antenne_unifie.py"
    "tableau_terminal.py"
    "components.py"
    "gamepad.py"
    "antenne.py"
    "$MAIN_FILE"
)

# Ajouter simulation_helper.py seulement si nécessaire (pour compatibilité)
ESSENTIAL_FILES+=("simulation_helper.py")

# Uploader seulement les fichiers essentiels
for filename in "${ESSENTIAL_FILES[@]}"; do
    filepath="$SOURCE_DIR/$filename"
    if [[ -f "$filepath" ]]; then
        if [[ "$filename" == "$MAIN_FILE" ]]; then
            echo "put $filepath main.py" >> "$TMP_MPSH"
        else
            echo "put $filepath $filename" >> "$TMP_MPSH"
        fi
    else
        echo "⚠️  Fichier manquant: $filename"
    fi
done

echo "exit" >> "$TMP_MPSH"

# 5. Exécuter le script
mpfshell -n -f "$TMP_MPSH"

# 6. Nettoyage
rm "$TMP_MPSH"

echo "✅ Déploiement terminé sur $TARGET_PORT"

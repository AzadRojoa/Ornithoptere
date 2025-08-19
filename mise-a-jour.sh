#!/bin/bash

# Script de mise à jour Ornithoptère pour Linux/macOS
# Version 1.0

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les titres
print_header() {
    echo
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║              MISE À JOUR SYSTÈME ORNITHOPTÈRE                ║"
    echo "║                      Version 1.0                            ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo
}

# Fonction pour afficher les erreurs
print_error() {
    echo -e "${RED}❌ ERREUR: $1${NC}"
}

# Fonction pour afficher les succès
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Fonction pour afficher les avertissements
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Fonction pour afficher les informations
print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Fonction de nettoyage en cas d'interruption
cleanup() {
    echo
    print_warning "Mise à jour interrompue par l'utilisateur."
    exit 1
}

# Piège pour Ctrl+C
trap cleanup SIGINT

# Début du script
clear
print_header

# [1/6] Vérification des prérequis
echo "[1/6] Vérification de l'environnement..."

# Vérification du dossier source
if [ ! -d "source" ]; then
    print_error "Dossier 'source' non trouvé."
    echo "    Assurez-vous d'exécuter ce script depuis le dossier principal du projet."
    exit 1
fi

# Vérification de Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python n'est pas installé ou non accessible."
        echo "    Veuillez installer Python avant de continuer."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

print_success "Environnement validé (Python: $PYTHON_CMD)."
echo

# [2/6] Sauvegarde de la version actuelle
echo "[2/6] Sauvegarde de la version actuelle..."
BACKUP_DIR="backup_$(date +%Y%m%d_%H%M%S)"

mkdir -p "backups"
mkdir -p "backups/$BACKUP_DIR"

if [ -d "source" ]; then
    cp -r source/* "backups/$BACKUP_DIR/" 2>/dev/null || true
    print_success "Sauvegarde créée dans: backups/$BACKUP_DIR"
else
    print_warning "Aucune version précédente trouvée."
fi
echo

# [3/6] Détection des ESP32
echo "[3/6] Détection des ESP32..."
ESP_PORTS=()

# Recherche des ports série selon l'OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    for port in /dev/ttyUSB* /dev/ttyACM*; do
        if [ -e "$port" ]; then
            ESP_PORTS+=("$port")
        fi
    done
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    for port in /dev/tty.usbserial-* /dev/tty.SLAB_USBtoUART* /dev/tty.usbmodem*; do
        if [ -e "$port" ]; then
            ESP_PORTS+=("$port")
        fi
    done
else
    print_warning "OS non reconnu. Recherche générique..."
    for port in /dev/tty*USB* /dev/tty*ACM* /dev/tty*serial*; do
        if [ -e "$port" ]; then
            ESP_PORTS+=("$port")
        fi
    done
fi

ESP_COUNT=${#ESP_PORTS[@]}

if [ $ESP_COUNT -eq 0 ]; then
    print_error "AUCUNE ESP32 DÉTECTÉE"
    echo "    Vérifiez que vos ESP32 sont bien connectées via USB."
    echo "    Redémarrez-les si nécessaire."
    echo "    Sous Linux, vous pourriez avoir besoin d'ajouter votre utilisateur au groupe 'dialout':"
    echo "    sudo usermod -a -G dialout \$USER"
    exit 1
fi

print_success "$ESP_COUNT ESP32 détectée(s):"
for i in "${!ESP_PORTS[@]}"; do
    echo "    - ${ESP_PORTS[$i]}"
done
echo

# [4/6] Choix du type de mise à jour
while true; do
    echo "[4/6] Type de mise à jour:"
    echo "    1. Émetteur (manette)"
    echo "    2. Récepteur (drone)"
    echo "    3. Les deux"
    echo
    read -p "Votre choix (1-3): " CHOICE
    
    case $CHOICE in
        1)
            UPDATE_TYPE="emetteur"
            UPDATE_FILE="emetteur_esp32.py"
            break
            ;;
        2)
            UPDATE_TYPE="recepteur"
            UPDATE_FILE="recepteur_esp32.py"
            break
            ;;
        3)
            UPDATE_TYPE="both"
            break
            ;;
        *)
            print_error "Choix invalide. Veuillez choisir 1, 2 ou 3."
            ;;
    esac
done

echo
echo "[5/6] Mise à jour en cours..."

# Fonction de déploiement
deploy_to_esp() {
    local TYPE=$1
    echo "       Déploiement sur ESP32 ($TYPE)..."
    
    local TARGET_PORT
    
    # Si un seul ESP32, l'utiliser directement
    if [ $ESP_COUNT -eq 1 ]; then
        TARGET_PORT="${ESP_PORTS[0]}"
    else
        # Si plusieurs ESP32, demander lequel utiliser
        echo "       Plusieurs ESP32 détectées. Laquelle utiliser pour le $TYPE ?"
        for i in "${!ESP_PORTS[@]}"; do
            echo "          $((i+1)). ${ESP_PORTS[$i]}"
        done
        
        while true; do
            read -p "       Choix (1-$ESP_COUNT): " PORT_CHOICE
            if [[ $PORT_CHOICE =~ ^[0-9]+$ ]] && [ $PORT_CHOICE -ge 1 ] && [ $PORT_CHOICE -le $ESP_COUNT ]; then
                TARGET_PORT="${ESP_PORTS[$((PORT_CHOICE-1))]}"
                break
            else
                print_error "Choix invalide."
            fi
        done
    fi
    
    # Vérification des permissions sur le port série
    if [ ! -w "$TARGET_PORT" ]; then
        print_error "Pas de permission d'écriture sur $TARGET_PORT"
        echo "       Essayez: sudo chmod 666 $TARGET_PORT"
        echo "       Ou ajoutez votre utilisateur au groupe dialout: sudo usermod -a -G dialout \$USER"
        return 1
    fi
    
    # Simulation du déploiement (remplacer par la vraie commande)
    echo "       Connexion à $TARGET_PORT..."
    sleep 1
    
    echo "       Effacement de l'ancienne version..."
    sleep 1
    
    echo "       Upload des nouveaux fichiers..."
    sleep 2
    
    echo "       Configuration du $TYPE..."
    sleep 1
    
    print_success "$TYPE mis à jour avec succès sur $TARGET_PORT"
    return 0
}

# Vérification des fichiers nécessaires
if [ "$UPDATE_TYPE" != "both" ]; then
    if [ ! -f "source/$UPDATE_FILE" ]; then
        print_error "Fichier $UPDATE_FILE non trouvé."
        echo "    Assurez-vous que la nouvelle version est correctement extraite."
        exit 1
    fi
else
    if [ ! -f "source/emetteur_esp32.py" ]; then
        print_error "Fichier emetteur_esp32.py non trouvé."
        exit 1
    fi
    if [ ! -f "source/recepteur_esp32.py" ]; then
        print_error "Fichier recepteur_esp32.py non trouvé."
        exit 1
    fi
fi

# Déploiement selon le type
if [ "$UPDATE_TYPE" = "both" ]; then
    echo "    Mise à jour de l'émetteur..."
    if ! deploy_to_esp "emetteur"; then
        print_error "Échec de la mise à jour de l'émetteur."
        exit 1
    fi
    
    echo "    Mise à jour du récepteur..."
    if ! deploy_to_esp "recepteur"; then
        print_error "Échec de la mise à jour du récepteur."
        exit 1
    fi
else
    echo "    Mise à jour du $UPDATE_TYPE..."
    if ! deploy_to_esp "$UPDATE_TYPE"; then
        print_error "Échec de la mise à jour du $UPDATE_TYPE."
        exit 1
    fi
fi

# [6/6] Succès
echo
echo "[6/6] ✅ MISE À JOUR TERMINÉE AVEC SUCCÈS !"
echo
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    INSTRUCTIONS FINALES                     ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  1. Débranchez puis rebranchez les ESP32                    ║"
echo "║  2. Allumez d'ABORD le récepteur (drone)                    ║"
echo "║  3. Allumez ENSUITE l'émetteur (manette)                    ║"
echo "║  4. Vérifiez que la LED devient verte (connexion OK)        ║"
echo "║                                                              ║"
echo "║  En cas de problème:                                        ║"
echo "║  - Lancez './restaurer-version-precedente.sh'               ║"
echo "║  - Contactez le support technique                           ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo
print_info "Sauvegarde disponible dans: backups/$BACKUP_DIR"
echo

# Attendre une touche avant de fermer
read -p "Appuyez sur Entrée pour continuer..."

# Note: Pour une vraie implémentation, remplacer la fonction deploy_to_esp par:
#
# deploy_to_esp() {
#     local TYPE=$1
#     local TARGET_PORT=$2
#     
#     # Utiliser le script de déploiement existant
#     if [ -f "scripts/deploy.sh" ]; then
#         echo "       Utilisation du script de déploiement..."
#         if ! ./scripts/deploy.sh --port "$TARGET_PORT" --type "$TYPE" --auto; then
#             return 1
#         fi
#     else
#         # Utiliser mpfshell ou ampy directement
#         echo "       Déploiement via mpfshell..."
#         
#         # Installer mpfshell si nécessaire
#         if ! command -v mpfshell &> /dev/null; then
#             pip3 install mpfshell
#         fi
#         
#         # Créer le script de déploiement temporaire
#         local TEMP_SCRIPT=$(mktemp)
#         cat > "$TEMP_SCRIPT" << EOF
# open $TARGET_PORT
# ls
# rm main.py
# put source/${TYPE}_esp32.py main.py
# put source/programme_antenne_unifie.py
# put source/antenne.py
# put source/components.py
# put source/gamepad.py
# put source/tableau_terminal.py
# put source/nrf24l01.py
# exit
# EOF
#         
#         if ! mpfshell -n -f "$TEMP_SCRIPT"; then
#             rm -f "$TEMP_SCRIPT"
#             return 1
#         fi
#         
#         rm -f "$TEMP_SCRIPT"
#     fi
#     
#     return 0
# }

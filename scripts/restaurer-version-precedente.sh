#!/bin/bash

# Script de restauration Ornithoptère pour Linux/macOS
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
    echo "║           RESTAURATION VERSION PRÉCÉDENTE                   ║"
    echo "║               Système Ornithoptère                          ║"
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
    print_warning "Restauration interrompue par l'utilisateur."
    exit 1
}

# Piège pour Ctrl+C
trap cleanup SIGINT

# Début du script
clear
print_header

# [1/4] Vérification du dossier de sauvegarde
if [ ! -d "backups" ]; then
    print_error "Aucune sauvegarde trouvée."
    echo "    Le dossier 'backups' n'existe pas."
    exit 1
fi

# Lister les sauvegardes disponibles
echo "[1/4] Recherche des sauvegardes disponibles..."
BACKUPS=()
BACKUP_COUNT=0

# Collecter les dossiers de sauvegarde
for backup_dir in backups/backup_*; do
    if [ -d "$backup_dir" ]; then
        BACKUPS+=("$(basename "$backup_dir")")
        BACKUP_COUNT=$((BACKUP_COUNT + 1))
        echo "    $BACKUP_COUNT. $(basename "$backup_dir")"
    fi
done

if [ $BACKUP_COUNT -eq 0 ]; then
    print_error "AUCUNE SAUVEGARDE TROUVÉE"
    echo "    Aucune version précédente n'est disponible pour la restauration."
    exit 1
fi

echo
print_success "$BACKUP_COUNT sauvegarde(s) trouvée(s)."
echo

# [2/4] Choix de la sauvegarde à restaurer
if [ $BACKUP_COUNT -eq 1 ]; then
    SELECTED_BACKUP="${BACKUPS[0]}"
    print_info "Sauvegarde sélectionnée automatiquement: $SELECTED_BACKUP"
else
    while true; do
        read -p "Quelle sauvegarde restaurer ? (1-$BACKUP_COUNT) ou 0 pour annuler: " BACKUP_CHOICE
        
        if [ "$BACKUP_CHOICE" = "0" ]; then
            echo "Restauration annulée."
            exit 0
        fi
        
        if [[ $BACKUP_CHOICE =~ ^[0-9]+$ ]] && [ $BACKUP_CHOICE -ge 1 ] && [ $BACKUP_CHOICE -le $BACKUP_COUNT ]; then
            SELECTED_BACKUP="${BACKUPS[$((BACKUP_CHOICE-1))]}"
            break
        else
            print_error "Choix invalide. Veuillez choisir entre 1 et $BACKUP_COUNT."
        fi
    done
fi

# Confirmation de la restauration
echo
echo "[2/4] Confirmation de la restauration..."
echo
print_warning "ATTENTION: Cette opération va:"
echo "    - Remplacer la version actuelle par: $SELECTED_BACKUP"
echo "    - Perdre tous les changements non sauvegardés"
echo

while true; do
    read -p "Êtes-vous sûr de vouloir continuer ? (O/N): " CONFIRM
    case $CONFIRM in
        [OoYy]* )
            break
            ;;
        [Nn]* )
            echo "Restauration annulée."
            exit 0
            ;;
        * )
            echo "Veuillez répondre par O (oui) ou N (non)."
            ;;
    esac
done

# [3/4] Sauvegarde de la version actuelle avant restauration
echo
echo "[3/4] Sauvegarde de la version actuelle..."
CURRENT_BACKUP="backup_avant_restauration_$(date +%Y%m%d_%H%M%S)"

mkdir -p "backups/$CURRENT_BACKUP"

if [ -d "source" ]; then
    cp -r source/* "backups/$CURRENT_BACKUP/" 2>/dev/null || true
    print_success "Version actuelle sauvegardée dans: $CURRENT_BACKUP"
fi

# [4/4] Restauration
echo
echo "[4/4] Restauration en cours..."
echo "    Suppression de la version actuelle..."
if [ -d "source" ]; then
    rm -rf source
fi

echo "    Restauration de $SELECTED_BACKUP..."
mkdir -p source

if ! cp -r "backups/$SELECTED_BACKUP/"* source/ 2>/dev/null; then
    print_error "Erreur lors de la restauration."
    echo "    Tentative de récupération..."
    if [ -d "backups/$CURRENT_BACKUP" ]; then
        cp -r "backups/$CURRENT_BACKUP/"* source/ 2>/dev/null || true
        print_warning "Version actuelle restaurée."
    fi
    exit 1
fi

print_success "Restauration terminée avec succès !"
echo

# Détection des ESP32 pour redéploiement
echo "Redéploiement sur les ESP32..."
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
fi

ESP_COUNT=${#ESP_PORTS[@]}

if [ $ESP_COUNT -eq 0 ]; then
    print_warning "Aucune ESP32 détectée."
    echo "    Connectez vos ESP32 et relancez './mise-a-jour.sh' pour les programmer."
else
    print_success "$ESP_COUNT ESP32 détectée(s)."
    echo
    
    while true; do
        read -p "Voulez-vous redéployer immédiatement sur les ESP32 ? (O/N): " REDEPLOY
        case $REDEPLOY in
            [OoYy]* )
                echo "Lancement de la mise à jour..."
                if [ -x "./mise-a-jour.sh" ]; then
                    ./mise-a-jour.sh
                else
                    print_warning "Script mise-a-jour.sh non trouvé ou non exécutable."
                    echo "    Rendez-le exécutable avec: chmod +x mise-a-jour.sh"
                fi
                break
                ;;
            [Nn]* )
                break
                ;;
            * )
                echo "Veuillez répondre par O (oui) ou N (non)."
                ;;
        esac
    done
fi

# Succès final
echo
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                 RESTAURATION TERMINÉE                       ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  Version restaurée: $SELECTED_BACKUP"
# Ajuster l'espacement selon la longueur du nom
SPACES_NEEDED=$((34 - ${#SELECTED_BACKUP}))
for ((i=1; i<=SPACES_NEEDED; i++)); do
    echo -n " "
done
echo "║"
echo "║                                                              ║"
echo "║  Prochaines étapes:                                         ║"
echo "║  1. Si pas encore fait, programmez les ESP32                ║"
echo "║  2. Testez le fonctionnement du système                     ║"
echo "║                                                              ║"
echo "║  Sauvegardes disponibles dans le dossier 'backups/'         ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo

# Attendre une touche avant de fermer
read -p "Appuyez sur Entrée pour continuer..."

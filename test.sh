#!/bin/bash

# Script de gestion des tests pour Ornithoptere
# Usage: ./test.sh [command]

set -e  # Arrêter en cas d'erreur

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'aide
show_help() {
    echo -e "${BLUE}🧪 Script de tests pour Ornithoptere${NC}"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commandes disponibles:"
    echo -e "  ${GREEN}test${NC}           Exécuter tous les tests unitaires"
    echo -e "  ${GREEN}test-module${NC}    Exécuter les tests d'un module spécifique"
    echo -e "  ${GREEN}coverage${NC}       Exécuter les tests avec mesure de couverture"
    echo -e "  ${GREEN}clean${NC}          Nettoyer les fichiers temporaires"
    echo -e "  ${GREEN}install-deps${NC}   Installer les dépendances de test"
    echo -e "  ${GREEN}help${NC}           Afficher cette aide"
    echo ""
    echo "Exemples:"
    echo "  $0 test                    # Tous les tests"
    echo "  $0 test-module bouton      # Tests du module bouton"
    echo "  $0 coverage                # Tests avec couverture"
}

# Fonction pour exécuter tous les tests
run_tests() {
    echo -e "${BLUE}🧪 Exécution de tous les tests unitaires...${NC}"
    cd "$(dirname "$0")"
    python3 tests/run_tests_simple.py
}

# Fonction pour exécuter les tests d'un module spécifique
run_module_tests() {
    local module=$1
    if [ -z "$module" ]; then
        echo -e "${RED}❌ Erreur: Nom du module requis${NC}"
        echo "Modules disponibles: bouton, logger, joystick, moteur, servomoteurs, antenne"
        exit 1
    fi
    
    echo -e "${BLUE}🧪 Exécution des tests pour le module: $module${NC}"
    cd "$(dirname "$0")"
    
    case $module in
        "bouton")
            python3 tests/test_bouton.py
            ;;
        "logger")
            python3 tests/test_logger.py
            ;;
        "joystick")
            python3 tests/test_joystick_simple.py
            ;;
        "moteur")
            python3 tests/test_moteur_simple.py
            ;;
        "servomoteurs")
            python3 tests/test_servomoteurs_simple.py
            ;;
        "antenne")
            python3 tests/test_antenne_simple.py
            ;;
        *)
            echo -e "${RED}❌ Module '$module' non reconnu${NC}"
            echo "Modules disponibles: bouton, logger, joystick, moteur, servomoteurs, antenne"
            exit 1
            ;;
    esac
}

# Fonction pour exécuter les tests avec couverture
run_coverage() {
    echo -e "${BLUE}📊 Exécution des tests avec mesure de couverture...${NC}"
    cd "$(dirname "$0")"
    
    # Vérifier si coverage est installé
    if ! command -v coverage &> /dev/null; then
        echo -e "${YELLOW}⚠️  coverage n'est pas installé. Installation...${NC}"
        pip3 install coverage
    fi
    
    python3 tests/run_tests_coverage.py
}

# Fonction pour nettoyer
clean() {
    echo -e "${BLUE}🧹 Nettoyage des fichiers temporaires...${NC}"
    cd "$(dirname "$0")"
    
    # Supprimer les fichiers de couverture
    rm -f .coverage
    rm -rf htmlcov/
    
    # Supprimer les caches Python
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -name "*.pyc" -delete 2>/dev/null || true
    
    # Supprimer les logs de test
    rm -f tests/*.log
    rm -f *.log
    
    echo -e "${GREEN}✅ Nettoyage terminé${NC}"
}

# Fonction pour installer les dépendances
install_deps() {
    echo -e "${BLUE}📦 Installation des dépendances de test...${NC}"
    cd "$(dirname "$0")"
    
    if [ -f "tests/requirements-test.txt" ]; then
        pip3 install -r tests/requirements-test.txt
        echo -e "${GREEN}✅ Dépendances installées${NC}"
    else
        echo -e "${YELLOW}⚠️  Fichier requirements-test.txt non trouvé${NC}"
        echo "Installation manuelle de coverage..."
        pip3 install coverage
    fi
}

# Parser les arguments
case "${1:-test}" in
    "test")
        run_tests
        ;;
    "test-module")
        run_module_tests "$2"
        ;;
    "coverage")
        run_coverage
        ;;
    "clean")
        clean
        ;;
    "install-deps")
        install_deps
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo -e "${RED}❌ Commande inconnue: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

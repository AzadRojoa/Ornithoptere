#!/bin/bash

# 🚀 SCRIPT D'INSTALLATION AUTOMATIQUE - Projet Ornithoptère
# ==========================================================
# Ce script installe AUTOMATIQUEMENT tout ce qui est nécessaire
# pour faire fonctionner le projet, même si vous êtes débutant !

set -e  # Arrêt en cas d'erreur

# Couleurs pour l'affichage
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
cat << "EOF"
   ____            _ _   _                   _
  / __ \          (_) | | |                 | |
 | |  | |_ __ _ __  _| |_| |__   ___  _ __  | |_ ___ _ __ ___
 | |  | | '__| '_ \| | __| '_ \ / _ \| '_ \ | __/ _ \ '__/ _ \
 | |__| | |  | | | | | |_| | | | (_) | |_) || ||  __/ | |  __/
  \____/|_|  |_| |_|_|\__|_| |_|\___/| .__/  \__\___|_|  \___|
                                     | |
                                     |_|
EOF
echo -e "${NC}"

echo -e "${BLUE}🚀 INSTALLATION AUTOMATIQUE DU PROJET ORNITHOPTÈRE${NC}"
echo "=================================================="
echo ""
echo -e "${GREEN}✨ Ce script va installer TOUT automatiquement !${NC}"
echo ""
echo "📋 Ce qui sera installé :"
echo "  • Dépendances système (Python, Git, etc.)"
echo "  • Environnement de développement complet"
echo "  • Outils de simulation PC"
echo "  • Outils de déploiement ESP32"
echo ""
echo -e "${YELLOW}⏱️  Durée estimée : 2-3 minutes${NC}"
echo ""

# Demander confirmation
read -p "Voulez-vous continuer ? [O/n] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[OoYy]?$ ]]; then
    echo "Installation annulée."
    exit 1
fi

echo ""
echo -e "${BLUE}🔧 ÉTAPE 1/5 : Mise à jour du système${NC}"
echo "=================================="

# Vérifier si on est sur Ubuntu/Debian
if ! command -v apt &> /dev/null; then
    echo -e "${RED}❌ Ce script est conçu pour Ubuntu/Debian${NC}"
    echo "   Vous devrez installer manuellement :"
    echo "   - Python 3, git, tmux, screen, socat"
    exit 1
fi

echo "📦 Mise à jour des paquets..."
sudo apt update -qq

echo ""
echo -e "${BLUE}🔧 ÉTAPE 2/5 : Installation des dépendances système${NC}"
echo "=============================================="

PACKAGES="python3 python3-venv python3-pip git tmux screen socat"
echo "📦 Installation : $PACKAGES"

# Installation silencieuse avec gestion d'erreur
if sudo apt install -y $PACKAGES > /dev/null 2>&1; then
    echo -e "✅ ${GREEN}Dépendances système installées${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'installation des dépendances système${NC}"
    echo "   Essayez d'exécuter manuellement :"
    echo "   sudo apt install $PACKAGES"
    exit 1
fi

echo ""
echo -e "${BLUE}🔧 ÉTAPE 3/5 : Configuration de l'environnement Python${NC}"
echo "================================================="

# Créer l'environnement virtuel
if [ -d ".venv" ]; then
    echo "♻️  Environnement virtuel existant détecté, suppression..."
    rm -rf .venv
fi

echo "🐍 Création de l'environnement virtuel..."
python3 -m venv .venv

echo "🔗 Activation de l'environnement..."
source .venv/bin/activate

echo "📦 Mise à jour de pip..."
pip install --upgrade pip > /dev/null 2>&1

echo -e "✅ ${GREEN}Environnement Python configuré${NC}"

echo ""
echo -e "${BLUE}🔧 ÉTAPE 4/5 : Installation des dépendances Python${NC}"
echo "=============================================="

echo "📚 Installation des outils de développement..."
if pip install -r requirements-dev.txt > /dev/null 2>&1; then
    echo -e "✅ ${GREEN}Outils de développement installés${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'installation des dépendances de développement${NC}"
    exit 1
fi

echo "🔌 Installation des outils de simulation..."
if pip install -r requirements.txt > /dev/null 2>&1; then
    echo -e "✅ ${GREEN}Outils de simulation installés${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'installation des dépendances de simulation${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}🔧 ÉTAPE 5/5 : Configuration des outils de qualité${NC}"
echo "==========================================="

echo "🪝 Installation des hooks pre-commit..."
if pre-commit install > /dev/null 2>&1; then
    echo -e "✅ ${GREEN}Hooks pre-commit installés${NC}"
else
    echo -e "${RED}❌ Erreur lors de l'installation des hooks pre-commit${NC}"
    exit 1
fi

echo "🧪 Test des hooks..."
if pre-commit run --all-files > /dev/null 2>&1; then
    echo -e "✅ ${GREEN}Hooks pre-commit fonctionnels${NC}"
else
    echo -e "${YELLOW}⚠️  Hooks installés mais certains tests ont échoué (normal lors de la première installation)${NC}"
fi

echo ""
echo -e "${GREEN}🎉 INSTALLATION TERMINÉE AVEC SUCCÈS !${NC}"
echo "======================================"
echo ""

# Test final
echo "🔍 Vérification finale..."
if ./scripts/check-dependencies.sh > /dev/null 2>&1; then
    echo -e "✅ ${GREEN}Tous les composants sont opérationnels !${NC}"
else
    echo -e "${YELLOW}⚠️  Installation réussie mais quelques ajustements peuvent être nécessaires${NC}"
fi

echo ""
echo -e "${BLUE}📚 COMMENT UTILISER LE PROJET MAINTENANT :${NC}"
echo "========================================"
echo ""
echo -e "${GREEN}1. Pour développer (à chaque session) :${NC}"
echo -e "   ${YELLOW}source .venv/bin/activate${NC}"
echo ""
echo -e "${GREEN}2. Pour tester votre code :${NC}"
echo -e "   ${YELLOW}./scripts/run-tests.sh${NC}"
echo ""
echo -e "${GREEN}3. Pour utiliser la simulation PC :${NC}"
echo "   • Changez SIMULATION = True dans vos programmes Python"
echo -e "   • Lancez : ${YELLOW}./simulation_pc/creer_ports_serie.sh${NC} (dans un terminal)"
echo -e "   • Lancez vos programmes : ${YELLOW}python3 source/programme_antenne_*.py${NC}"
echo ""
echo -e "${GREEN}4. Pour déployer sur ESP32 :${NC}"
echo -e "   • Connectez vos ESP32 en USB"
echo -e "   • Lancez : ${YELLOW}./scripts/deploy.sh${NC}"
echo ""
echo -e "${GREEN}5. Pour surveiller les ESP32 :${NC}"
echo -e "   • Lancez : ${YELLOW}./scripts/start.sh${NC}"
echo ""
echo -e "${BLUE}📖 DOCUMENTATION COMPLÈTE :${NC}"
echo "=========================="
echo -e "• Guide détaillé : ${YELLOW}docs/setup.md${NC}"
echo -e "• Mode simulation : ${YELLOW}docs/simulation.md${NC}"
echo -e "• Dépannage : ${YELLOW}docs/TROUBLESHOOTING.md${NC}"
echo -e "• Vérifier installation : ${YELLOW}./scripts/check-dependencies.sh${NC}"
echo ""
echo -e "${GREEN}🎊 Bon développement !${NC}"

# Désactiver l'environnement pour ne pas influencer le shell de l'utilisateur
deactivate 2>/dev/null || true

echo ""
echo -e "${YELLOW}💡 RAPPEL : Pour développer, commencez toujours par :${NC}"
echo -e "${YELLOW}   source .venv/bin/activate${NC}"

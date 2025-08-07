#!/bin/bash
# Script de vérification des dépendances pour le projet Ornithoptère

echo "🔍 VÉRIFICATION DES DÉPENDANCES - Projet Ornithoptère"
echo "=================================================="
echo ""

# Couleurs pour l'affichage
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

success=0
errors=0

check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "✅ ${GREEN}$1${NC} - $(command -v "$1")"
        ((success++))
    else
        echo -e "❌ ${RED}$1 manquant${NC}"
        ((errors++))
        if [ -n "$2" ]; then
            echo -e "   💡 Installation: ${YELLOW}$2${NC}"
        fi
    fi
}

echo "🖥️  Dépendances système :"
echo "-----------------------"
check_command "python3" "sudo apt install python3"
check_command "pip3" "sudo apt install python3-pip"
check_command "git" "sudo apt install git"
check_command "tmux" "sudo apt install tmux"
check_command "screen" "sudo apt install screen"
check_command "socat" "sudo apt install socat"
echo ""

echo "🐍 Dépendances Python globales :"
echo "--------------------------------"
if pip3 list 2>/dev/null | grep -q pyserial; then
    version=$(pip3 show pyserial 2>/dev/null | grep Version | cut -d' ' -f2)
    echo -e "✅ ${GREEN}pyserial${NC} - version $version"
    ((success++))
else
    echo -e "❌ ${RED}pyserial manquant${NC}"
    echo -e "   💡 Installation: ${YELLOW}pip3 install pyserial${NC}"
    ((errors++))
fi

if pip3 list 2>/dev/null | grep -q mpfshell; then
    version=$(pip3 show mpfshell 2>/dev/null | grep Version | cut -d' ' -f2)
    echo -e "✅ ${GREEN}mpfshell${NC} - version $version"
    ((success++))
else
    echo -e "⚠️  ${YELLOW}mpfshell absent${NC} (optionnel pour ESP32)"
    echo -e "   💡 Installation: ${YELLOW}pip3 install mpfshell${NC}"
fi
echo ""

echo "📁 Environnement virtuel :"
echo "-------------------------"
if [ -d ".venv" ]; then
    echo -e "✅ ${GREEN}Environnement virtuel trouvé${NC} - .venv/"
    ((success++))

    # Vérification des dépendances dans le venv
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate

        echo "📦 Packages dans l'environnement virtuel :"
        dev_packages=("pre-commit" "flake8" "black" "isort" "mypy" "pytest" "pytest-cov")

        for pkg in "${dev_packages[@]}"; do
            if pip list 2>/dev/null | grep -q "$pkg"; then
                version=$(pip show "$pkg" 2>/dev/null | grep Version | cut -d' ' -f2)
                echo -e "   ✅ ${GREEN}$pkg${NC} - version $version"
                ((success++))
            else
                echo -e "   ❌ ${RED}$pkg manquant${NC}"
                ((errors++))
            fi
        done

        # Check si pyserial est dans le venv (pour simulation)
        if pip list 2>/dev/null | grep -q pyserial; then
            version=$(pip show pyserial 2>/dev/null | grep Version | cut -d' ' -f2)
            echo -e "   ✅ ${GREEN}pyserial${NC} - version $version (simulation)"
            ((success++))
        fi

        deactivate 2>/dev/null || true
    fi
else
    echo -e "❌ ${RED}Environnement virtuel manquant${NC}"
    echo -e "   💡 Création: ${YELLOW}python3 -m venv .venv${NC}"
    ((errors++))
fi
echo ""

echo "🔧 Configuration pre-commit :"
echo "----------------------------"
if [ -f ".pre-commit-config.yaml" ]; then
    echo -e "✅ ${GREEN}Configuration pre-commit trouvée${NC}"
    ((success++))

    if [ -d ".git/hooks" ] && [ -f ".git/hooks/pre-commit" ]; then
        echo -e "✅ ${GREEN}Hooks pre-commit installés${NC}"
        ((success++))
    else
        echo -e "⚠️  ${YELLOW}Hooks pre-commit non installés${NC}"
        echo -e "   💡 Installation: ${YELLOW}pre-commit install${NC}"
    fi
else
    echo -e "❌ ${RED}Configuration pre-commit manquante${NC}"
    ((errors++))
fi
echo ""

echo "🧪 Vérification des tests :"
echo "--------------------------"
if [ -d "source/tests" ]; then
    echo -e "✅ ${GREEN}Dossier tests trouvé${NC}"
    ((success++))

    test_files=$(find source/tests -name "test_*.py" | wc -l)
    echo -e "   📄 $test_files fichiers de test trouvés"

    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        if command -v pytest &> /dev/null; then
            echo -e "   🧪 Test rapide des imports..."
            cd source && python -c "
try:
    import sys, os
    sys.path.insert(0, os.path.join('.', 'tests'))
    from mock_machine import machine
    print('   ✅ Mock machine OK')
    sys.modules['machine'] = machine
    from components import Joystick, Bouton
    print('   ✅ Imports components OK')
    from gamepad import Gamepad
    print('   ✅ Import gamepad OK')
except Exception as e:
    print(f'   ❌ Erreur import: {e}')
" && cd ..
        fi
        deactivate 2>/dev/null || true
    fi
else
    echo -e "❌ ${RED}Dossier tests manquant${NC}"
    ((errors++))
fi
echo ""

echo "📊 RÉSUMÉ :"
echo "=========="
echo -e "✅ ${GREEN}Succès: $success${NC}"
if [ $errors -gt 0 ]; then
    echo -e "❌ ${RED}Erreurs: $errors${NC}"
    echo ""
    echo -e "🚀 ${YELLOW}Pour une installation complète automatique :${NC}"
    echo -e "   ${YELLOW}./scripts/setup-precommit.sh${NC}"
    echo ""
    echo -e "📖 ${YELLOW}Pour plus d'infos, consultez :${NC}"
    echo -e "   ${YELLOW}./docs/setup.md${NC}"
    echo -e "   ${YELLOW}./docs/dependencies_audit.md${NC}"
    exit 1
else
    echo -e "🎉 ${GREEN}Toutes les dépendances sont OK !${NC}"
    echo ""
    echo -e "✨ ${GREEN}Le projet est prêt à être utilisé.${NC}"
    echo ""
    echo -e "🚀 ${YELLOW}Commandes utiles :${NC}"
    echo -e "   ${YELLOW}source .venv/bin/activate${NC}   # Activer l'environnement"
    echo -e "   ${YELLOW}./scripts/run-tests.sh${NC}      # Lancer les tests"
    echo -e "   ${YELLOW}pre-commit run --all-files${NC}  # Vérifier le code"
    echo -e "   ${YELLOW}./scripts/deploy.sh${NC}         # Déployer sur ESP32"
fi

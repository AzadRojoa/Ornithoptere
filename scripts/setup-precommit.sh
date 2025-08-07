#!/bin/bash

echo "🚀 Installation des hooks pre-commit pour Ornithoptere"
echo "=================================================="

# Vérification que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Création de l'environnement virtuel s'il n'existe pas
if [ ! -d ".venv" ]; then
    echo "🔧 Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# Activation de l'environnement virtuel
echo "🔗 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Installation des dépendances de développement
echo "📦 Installation des dépendances de développement..."
pip install --upgrade pip
pip install -r requirements-dev.txt

# Vérification que pre-commit est installé
if ! command -v pre-commit &> /dev/null; then
    echo "❌ pre-commit n'a pas pu être installé"
    exit 1
fi

# Installation des hooks pre-commit
echo "🔧 Installation des hooks pre-commit..."
pre-commit install

# Test des hooks
echo "✅ Test des hooks pre-commit..."
pre-commit run --all-files

echo ""
echo "🎉 Pre-commit configuré avec succès !"
echo ""
echo "Les hooks suivants seront exécutés avant chaque commit :"
echo "  - Formatage du code avec Black"
echo "  - Tri des imports avec isort"
echo "  - Vérification du linting avec flake8"
echo "  - Exécution des tests unitaires avec pytest"
echo "  - Vérifications générales (trailing whitespace, etc.)"
echo ""
echo "⚠️  Important : Activez l'environnement virtuel avant de commiter :"
echo "     source .venv/bin/activate"
echo ""
echo "Pour exécuter manuellement les hooks : pre-commit run --all-files"
echo "Pour bypasser les hooks (non recommandé) : git commit --no-verify"

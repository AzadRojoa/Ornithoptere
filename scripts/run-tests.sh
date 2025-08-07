#!/bin/bash
# Se déplacer vers le répertoire du projet (depuis le dossier scripts)
cd "$(dirname "$0")/.."
source .venv/bin/activate
python -m pytest source/tests/ -v

# Documentation des scripts : deploy.sh & start.sh

## deploy.sh

Ce script automatise le déploiement du code sur une carte ESP32/ESP8266 via mpfshell. Il permet :
- De choisir le programme à envoyer (émission ou réception).
- De détecter automatiquement les ports USB connectés.
- De supprimer les anciens fichiers sur la carte (sauf `boot.py`).
- D'uploader tous les fichiers nécessaires, en renommant le programme principal en `main.py`.
- De nettoyer les fichiers temporaires après le déploiement.

Ce script facilite la mise à jour rapide du code sur la carte sans intervention manuelle.

## start.sh

Ce script lance automatiquement une session tmux préconfigurée pour le développement et le monitoring :
- Ouvre trois panneaux tmux : deux pour les terminaux série (un par ESP, via `screen`), un libre pour les commandes.
- Configure la navigation à la souris dans tmux.
- Permet de surveiller simultanément l'émission et la réception sur les deux cartes.

Ce script est utile pour travailler efficacement avec plusieurs microcontrôleurs et garder un environnement organisé.

## release-push.sh

Ce script automatise le déploiement vers la branche `release` en ne poussant que les fichiers de production nécessaires (dossiers `source` et `docs`, ainsi que les fichiers `.gitignore`, `README.md`, `deploy.sh`, `requirements-test.txt` et `start.sh`). Il crée une branche release propre sans les fichiers de test et de développement.

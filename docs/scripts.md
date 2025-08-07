# Documentation des scripts (dossier `scripts/`)

## scripts/deploy.sh

Ce script automatise le déploiement du code sur une carte ESP32/ESP8266 via mpfshell. Il permet :
- De choisir le programme à envoyer (émission ou réception).
- De détecter automatiquement les ports USB connectés.
- De supprimer les anciens fichiers sur la carte (sauf `boot.py`).
- D'uploader tous les fichiers nécessaires, en renommant le programme principal en `main.py`.
- De nettoyer les fichiers temporaires après le déploiement.

Ce script facilite la mise à jour rapide du code sur la carte sans intervention manuelle.

**Usage :**
```bash
./scripts/deploy.sh
```

## scripts/start.sh

Ce script lance automatiquement une session tmux préconfigurée pour le développement et le monitoring :
- Ouvre trois panneaux tmux : deux pour les terminaux série (un par ESP, via `screen`), un libre pour les commandes.
- Configure la navigation à la souris dans tmux.
- Permet de surveiller simultanément l'émission et la réception sur les deux cartes.

**Usage :**
```bash
./scripts/start.sh
```

## scripts/setup-precommit.sh

Ce script configure automatiquement l'environnement de développement :
- Crée l'environnement virtuel Python
- Installe toutes les dépendances de développement
- Configure les hooks pre-commit
- Lance un test complet

**Usage :**
```bash
./scripts/setup-precommit.sh
```

## scripts/run-tests.sh

Ce script exécute tous les tests unitaires du projet.

**Usage :**
```bash
./scripts/run-tests.sh
```

## scripts/check-dependencies.sh

Ce script vérifie que toutes les dépendances nécessaires sont installées et configurées correctement. Il affiche un rapport détaillé de l'état du système et suggère les corrections nécessaires.

**Usage :**
```bash
./scripts/check-dependencies.sh
```

**Fonctionnalités :**
- Vérification des dépendances système (python3, git, tmux, socat, etc.)
- Contrôle des packages Python globaux et dans l'environnement virtuel
- Vérification de la configuration pre-commit
- Test des imports principaux du projet
- Rapport coloré avec suggestions d'installation scripts : deploy.sh & start.sh

## deploy.sh

Ce script automatise le déploiement du code sur une carte ESP32/ESP8266 via mpfshell. Il permet :
- De choisir le programme à envoyer (émission ou réception).
- De détecter automatiquement les ports USB connectés.
- De supprimer les anciens fichiers sur la carte (sauf `boot.py`).
- D’uploader tous les fichiers nécessaires, en renommant le programme principal en `main.py`.
- De nettoyer les fichiers temporaires après le déploiement.

Ce script facilite la mise à jour rapide du code sur la carte sans intervention manuelle.

## start.sh

Ce script lance automatiquement une session tmux préconfigurée pour le développement et le monitoring :
- Ouvre trois panneaux tmux : deux pour les terminaux série (un par ESP, via `screen`), un libre pour les commandes.
- Configure la navigation à la souris dans tmux.
- Permet de surveiller simultanément l’émission et la réception sur les deux cartes.

Ce script est utile pour travailler efficacement avec plusieurs microcontrôleurs et garder un environnement organisé.

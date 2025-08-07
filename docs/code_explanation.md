# Documentation technique du projet Ornithoptere

Ce projet permet de transmettre et recevoir des commandes pour piloter un ornithoptère (ou tout autre dispositif) à l'aide de modules radio NRF24L01 et d'un microcontrôleur compatible MicroPython (ESP32, ESP8266, etc).

## 📖 Documentation complète

- 🚀 [Guide de démarrage](quickstart.md) - Installation et première utilisation
- 🔧 [Configuration avancée](setup.md) - Installation et configuration détaillée
- 💻 [Mode simulation PC](simulation.md) - Testez sans ESP32 !
- 🔧 [Scripts et outils](scripts.md) - Automatisation du déploiement
- 🛠️ [Dépannage](TROUBLESHOOTING.md) - Résolution de problèmes

## Fonctionnalités

- Lecture de deux joysticks analogiques et de deux boutons.
- Transmission des valeurs lues via un module NRF24L01.
- Réception des commandes sur un autre module NRF24L01.
- Contrôle d'un moteur via la réception des commandes.
- Gestion de logs sur la carte.
- Abstraction des périphériques (joystick, bouton, servo-moteur) via des classes dédiées.
- **Mode simulation PC** : Testez sans ESP32 en utilisant des ports série virtuels.

## Structure du projet

- `source/programme_antenne_emission.py` : Code principal pour l'émetteur. Lit les joysticks et boutons, envoie les données via la classe `Antenne`.
- `source/programme_antenne_reception.py` : Code principal pour le récepteur. Reçoit les données, les interprète et contrôle un moteur.
- `source/antenne.py` : Classe `Antenne` pour gérer la communication radio (émission/réception) avec le NRF24L01.
- `source/components.py` : Classes pour abstraire les périphériques matériels :
  - `Joystick` : lecture de deux axes analogiques.
  - `Bouton` : gestion d'un bouton avec pull-up.
  - `ServoMoteur` : contrôle d'un servo-moteur via PWM.
  - `Moteur` : contrôle d'un moteur via PWM.
- `source/nrf24l01.py` : Pilote bas niveau pour le module radio NRF24L01.
- `source/logger.py` : Classe `Logger` pour enregistrer des logs sur la carte.

## Utilisation

### Émetteur

1. Connecter deux joysticks (axes X/Y sur les broches analogiques) et deux boutons.
2. Lancer `programme_antenne_emission.py` sur la carte émettrice.
3. Les valeurs des joysticks et boutons sont envoyées en continu via le module NRF24L01.

### Récepteur

1. Connecter un moteur (ou tout autre actionneur) sur la broche prévue.
2. Lancer `programme_antenne_reception.py` sur la carte réceptrice.
3. Les commandes reçues pilotent le moteur selon la valeur du bouton.

### Exemple de log

Utilisez la classe `Logger` pour enregistrer des événements ou erreurs dans un fichier texte sur la carte.

## Scripts de gestion

- `scripts/deploy.sh` : Automatisation du déploiement du code sur l'ESP (sélection du programme, upload, nettoyage des fichiers, renommage en main.py).
- `scripts/start.sh` : Ouverture automatique d'une session tmux avec les terminaux série pour surveiller les deux ESP et faciliter le développement.
- `scripts/setup-precommit.sh` : Installation automatique de l'environnement de développement avec pre-commit.
- `scripts/run-tests.sh` : Exécution des tests unitaires.

## Dépendances

- MicroPython
- Modules matériels : NRF24L01, joysticks analogiques, boutons, moteur ou servo-moteur.

## Schéma de câblage

- Les broches utilisées sont configurables dans les fichiers Python.
- Par défaut :
  - Joystick 1 : X=34, Y=35 ; bouton 1 : 33
  - Joystick 2 : X=36, Y=39 ; bouton 2 : 32
  - NRF24L01 : SPI1 (SCK=18, MOSI=23, MISO=19, CE=26, CSN=27)
  - Moteur : 5

## Personnalisation

- Modifiez les broches dans les constructeurs des classes selon votre câblage.
- Adaptez le traitement des messages reçus dans `programme_antenne_reception.py` selon vos besoins.

## Auteurs

Projet développé pour un usage pédagogique ou hobby autour de la radio et du contrôle.

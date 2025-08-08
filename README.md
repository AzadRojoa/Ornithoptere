# Ornithoptère - Système de Contrôle Radio

Ce projet permet de piloter un ornithoptère (ou autre dispositif) à distance via des modules radio NRF24L01 et des microcontrôleurs ESP32 compatibles MicroPython.

## 🎯 Vue d'ensemble

Le système comprend deux parties :
- **Émetteur** : Contrôleur avec joysticks pour envoyer les commandes
- **Récepteur** : Dispositif embarqué qui reçoit et exécute les commandes

Le projet inclut également un **mode simulation** complet permettant de développer et tester sans matériel physique.

## 📚 Documentation

### 🚀 Pour commencer
- **[🚀 Guide d'utilisation](docs/quickstart.md)** - Comment utiliser le projet (simulation, déploiement)
- **[� Dépendances](docs/dependencies.md)** - Liste des dépendances et installation

### 🛠️ Configuration
- **[🔧 Setup avancé](docs/setup.md)** - Installation et configuration pour développeurs expérimentés
- **[🏗️ Architecture](docs/architecture.md)** - Structure et fonctionnement du projet

### 🎮 Fonctionnalités avancées
- **[⌨️ Contrôle Clavier](docs/controle_clavier.md)** - Simulation avec contrôles clavier
- **[🧪 Simulation](docs/simulation.md)** - Mode simulation détaillé

### 🐛 Aide
- **[🐛 Dépannage](docs/TROUBLESHOOTING.md)** - Solutions aux problèmes courants


## 🚀 Démarrage rapide

### Mode Simulation (recommandé pour débuter)
```bash
# 1. Lancer les ports virtuels
./simulation_pc/creer_ports_serie.sh

# 2. Dans un autre terminal, activer la simulation
# Éditez source/programme_antenne_emission.py : SIMULATION = True
python3 source/programme_antenne_emission.py

# 3. Contrôlez avec le clavier : W/A/S/D, flèches, etc.
```

## 🛠️ Technologies

- **MicroPython** - Firmware pour ESP32
- **NRF24L01** - Modules radio 2.4GHz
- **Python 3** - Simulation PC
- **Gamepad/Joysticks** - Interface de contrôle

## 🤝 Contribution

1. Fork le projet
2. Créez une branche feature
3. Commitez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence libre. Voir le fichier LICENSE pour plus de détails.

---

**🎮 Amusez-vous bien avec votre ornithoptère !**

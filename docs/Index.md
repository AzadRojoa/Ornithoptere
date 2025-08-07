# 📚 Documentation - Projet Ornithoptère

## 🎯 Par niveau d'utilisateur

### 🚀 **Débutants - Commencer ici**
- **[Guide de démarrage rapide](quickstart.md)** - Installation et première utilisation en 5 minutes

### 👨‍💻 **Développeurs**
- **[Guide d'installation avancé](setup.md)** - Configuration personnalisée et environnement de dev
- **[Mode simulation PC](simulation.md)** - Tester sans hardware ESP32
- **[Architecture et code](code_explanation.md)** - Comment fonctionne le projet

### 🔧 **Experts/Administrateurs**
- **[Scripts et outils](scripts.md)** - Automatisation et déploiement
- **[Audit des dépendances](dependencies.md)** - Liste complète pour réinstallation
- **[Dépannage](TROUBLESHOOTING.md)** - Solutions aux problèmes courants

---

## 📋 Par besoin spécifique

| Besoin | Document |
|--------|----------|
| **Je veux juste que ça marche** | [Guide rapide](quickstart.md) |
| **J'ai des erreurs** | [Dépannage](TROUBLESHOOTING.md) |
| **Je développe le projet** | [Setup avancé](setup.md) |
| **Je veux comprendre le code** | [Architecture](code_explanation.md) |
| **Je teste sans ESP32** | [Mode simulation](simulation.md) |
| **Je réinstalle tout** | [Dépendances](dependencies.md) |
| **J'utilise les scripts** | [Scripts](scripts.md) |

---

## ⚡ Raccourcis commandes

```bash
# Installation automatique
./install.sh

# Vérifier l'installation
./test-install.sh

# Activer l'environnement (toujours)
source .venv/bin/activate

# Mode simulation
./simulation_pc/creer_ports_serie.sh

# Déployer sur ESP32
./scripts/deploy.sh
```

---

## 🗂️ Structure de la documentation

```
docs/
├── README.md                 ← Ce fichier (index)
├── quickstart.md            ← Guide débutant (COMMENCEZ ICI)
├── setup.md                 ← Installation avancée
├── simulation.md            ← Mode simulation PC
├── code_explanation.md      ← Architecture technique
├── scripts.md               ← Documentation des scripts
├── dependencies.md          ← Audit des dépendances
├── TROUBLESHOOTING.md       ← Dépannage
└── pinout.png              ← Schéma ESP32
```

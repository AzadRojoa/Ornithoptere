# 🚀 Guide de démarrage rapide - Ornithoptère

**Installation et première utilisation en 5 minutes !**

---

## ⚡ Installation automatique

```bash
git clone [URL_DU_PROJET]
cd Ornithoptere
./install.sh    # ← FAIT TOUT AUTOMATIQUEMENT !
```

**✨ Le script fait tout :** Python, outils, tests, configuration...

---

## 🎮 Première utilisation

### Option 1 : Mode Simulation PC (recommandé pour débuter)

```bash
# 1. Activer l'environnement (toujours faire ça en premier)
source .venv/bin/activate

# 2. Configurer la simulation
# Editez source/programme_antenne_emission.py et source/programme_antenne_reception.py
# Changez la ligne : SIMULATION = True

# 3. Lancer la simulation (3 terminaux)
./simulation_pc/creer_ports_serie.sh                    # Terminal 1 (gardez ouvert)
python3 source/programme_antenne_emission.py            # Terminal 2
python3 source/programme_antenne_reception.py           # Terminal 3
```

**✅ Avantages simulation :** Pas d'ESP32 nécessaire, débogage facile, test rapide

### Option 2 : Mode ESP32 réel (pour utilisateurs avancés)

```bash
# 1. Activer l'environnement
source .venv/bin/activate

# 2. Configurer pour ESP32 réel
# Dans vos programmes Python : SIMULATION = False

# 3. Connecter les ESP32 en USB et déployer
./scripts/deploy.sh     # Choisir émission/réception pour chaque ESP32

# 4. Surveiller les ESP32
./scripts/start.sh      # Ouvre tmux avec terminaux série
```

---

## 🛠️ Commandes utiles

| Action | Commande |
|--------|----------|
| **Tester l'installation** | `./test-install.sh` |
| **Vérifier les dépendances** | `./scripts/check-dependencies.sh` |
| **Lancer les tests** | `./scripts/run-tests.sh` |
| **Réinstaller proprement** | `rm -rf .venv && ./install.sh` |

---

## 🆘 En cas de problème

1. **Vérifier l'installation :** `./test-install.sh`
2. **Diagnostic détaillé :** `./scripts/check-dependencies.sh`
3. **Consulter le dépannage :** [docs/TROUBLESHOOTING.md](TROUBLESHOOTING.md)
4. **Réinstaller :** `rm -rf .venv && ./install.sh`

---

## 📚 Pour aller plus loin

- **[Setup avancé](setup.md)** - Configuration personnalisée
- **[Mode simulation détaillé](simulation.md)** - Tout sur la simulation PC
- **[Architecture du projet](code_explanation.md)** - Comment ça fonctionne
- **[Scripts et outils](scripts.md)** - Tous les outils disponibles

---

## 💡 Conseils

- 🔄 **Toujours commencer par :** `source .venv/bin/activate`
- 🧪 **Débuter par la simulation** (plus simple que ESP32)
- 📊 **Utiliser les scripts** (tout est automatisé !)
- 🔍 **En cas de doute :** `./test-install.sh`

### Mode 2 : ESP32 réels (pour experts)

```bash
# 1. Activer l'environnement
source .venv/bin/activate

# 2. Modifier vos programmes Python
# Changez : SIMULATION = False

# 3. Connecter vos ESP32 en USB

# 4. Déployer le code
./scripts/deploy.sh

# 5. Surveiller les ESP32
./scripts/start.sh
```

---

## 🆘 En cas de problème

### Vérifier que tout est bien installé :
```bash
./scripts/check-dependencies.sh
```

### Tester le code :
```bash
source .venv/bin/activate
./scripts/run-tests.sh
```

### Réinstaller complètement :
```bash
rm -rf .venv
./install.sh
```

---

## 📚 Documentation complète

Si vous voulez plus de détails :
- **[Guide complet](docs/setup.md)** - Toutes les options
- **[Mode simulation](docs/simulation.md)** - Détails simulation PC
- **[Dépannage](docs/TROUBLESHOOTING.md)** - Solutions aux problèmes
- **[Architecture](docs/code_explanation.md)** - Comment ça marche

---

## 💡 Conseils pour débuter

1. **Commencez par la simulation** - Plus facile à comprendre
2. **Activez toujours l'environnement** : `source .venv/bin/activate`
3. **Utilisez les scripts** - Tout est automatisé !
4. **En cas de doute** : `./scripts/check-dependencies.sh`

**Bon développement ! 🎊**

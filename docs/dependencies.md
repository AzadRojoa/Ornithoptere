# 📋 Dépendances - Projet Ornithoptère

> **💡 TL;DR :** Lancez `./install.sh` - il fait tout automatiquement !

---

## 🚀 Installation automatique (recommandée)

```bash
git clone [URL]
cd Ornithoptere
./install.sh    # ← Installe TOUT automatiquement
```

---

## 📦 Dépendances détaillées

### Système (Ubuntu/Debian)
```bash
sudo apt install -y python3 python3-venv python3-pip git tmux screen socat
```

| Package | Usage | Obligatoire |
|---------|-------|-------------|
| `python3` | Langage principal | ✅ |
| `python3-venv` | Environnements virtuels | ✅ |
| `python3-pip` | Gestionnaire packages | ✅ |
| `git` | Contrôle de version | ✅ |
| `tmux` | Terminal multiplexé ESP32 | Si hardware réel |
| `screen` | Accès série ESP32 | Si hardware réel |
| `socat` | Ports série simulation | Si simulation |

### Python (installées automatiquement)

**Simulation :**
- `pyserial>=3.5` - Communication série

**Développement :**
- `pre-commit`, `black`, `flake8`, `isort`, `mypy`, `pytest`, `pytest-cov`

**ESP32 :**
- `mpfshell>=0.9.1` - Déploiement sur microcontrôleurs

---

## 🔍 Vérification

```bash
# Diagnostic complet
./scripts/check-dependencies.sh

# Test d'installation
./test-install.sh
```

---

## 📚 Modules Python utilisés

### Standards (inclus avec Python)
`time`, `os`, `sys`, `json`, `logging`, `queue`, `threading`, `typing`, `unittest`

### MicroPython (ESP32 seulement)
`machine`, `micropython`, `utime`, `ujson`, `_thread`

### Projet (internes)
`components`, `gamepad`, `antenne`, `logger`, `tableau_terminal`, `flight_controler`, `nrf24l01`

---

## 🛠️ Installation manuelle (experts)

<details>
<summary>Cliquez pour les détails</summary>

```bash
# 1. Système
sudo apt update
sudo apt install -y python3 python3-venv python3-pip git tmux screen socat

# 2. Environnement Python
python3 -m venv .venv
source .venv/bin/activate

# 3. Dépendances Python
pip install -r requirements-dev.txt
pip install -r requirements.txt

# 4. Configuration pre-commit
pre-commit install

# 5. Test
./scripts/run-tests.sh
```

</details>

### Installation minimale (développement uniquement) :
```bash
sudo apt install python3 python3-venv python3-pip git
cd Ornithoptere && ./scripts/setup-precommit.sh
```

### Installation avec simulation :
```bash
sudo apt install python3 python3-venv python3-pip git socat
cd Ornithoptere && ./scripts/setup-precommit.sh
```

### Installation complète (ESP32 + simulation + dev) :
```bash
sudo apt install python3 python3-venv python3-pip git tmux screen socat
cd Ornithoptere && ./scripts/setup-precommit.sh
```

---

## 🔍 VÉRIFICATION

Pour vérifier que tout est installé :
```bash
./scripts/check-dependencies.sh
```

---

## 📝 FICHIERS CONCERNÉS

- `requirements.txt` - Dépendances simulation (pyserial)
- `requirements-dev.txt` - Dépendances développement + mpfshell
- `scripts/setup-precommit.sh` - Installation automatique
- `scripts/check-dependencies.sh` - Vérification
- `docs/dependencies_audit.md` - Documentation complète

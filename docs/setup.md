# 🔧 Configuration avancée - Ornithoptère

Ce guide s'adresse aux développeurs qui souhaitent une configuration personnalisée ou comprendre les détails techniques.

> **💡 Débutants :** Utilisez plutôt le [guide de démarrage rapide](quickstart.md)

---

## 🚀 Installation rapide

<details>
<summary><strong>📦 Installation automatique (recommandée)</strong></summary>

```bash
git clone [URL_DU_PROJET]
cd Ornithoptere
./install.sh     # ← Solution tout-en-un
```

**📖 Guide complet :** [docs/quickstart.md](quickstart.md)

</details>

<details>
<summary><strong>🛠️ Installation développeur (plus de contrôle)</strong></summary>

```bash
git clone [URL_DU_PROJET]
cd Ornithoptere
./scripts/setup-precommit.sh    # Installation environnement dev seulement
```

</details>

---

## 🛠️ Configuration de l'environnement de développement

### Pre-commit - Contrôle qualité automatique

Ce projet utilise **pre-commit** pour vérifier automatiquement votre code avant chaque commit :
- ✨ **Formatage automatique** (Black, isort)
- 🔍 **Vérification du style** (flake8)
- 🧪 **Exécution des tests** (pytest)

<details>
<summary><strong>Installation manuelle de pre-commit</strong></summary>

```bash
# Créer l'environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements-dev.txt

# Installer les hooks pre-commit
pre-commit install
```

</details>

<details>
<summary><strong>🔧 Dépannage pre-commit</strong></summary>

**Problèmes courants :**

- **❌ "Command not found: pre-commit"**
  ```bash
  source .venv/bin/activate
  ```

- **❌ Commit échoue avec "files were modified"**
  C'est normal ! Pre-commit a formaté votre code :
  ```bash
  git add .
  git commit -m "Votre message"
  ```

- **❌ Tests qui échouent**
  ```bash
  ./scripts/run-tests.sh  # Voir les erreurs
  # Corriger les erreurs puis recommiter
  ```

**Commandes utiles :**
```bash
# Tester tous les hooks
pre-commit run --all-files

# Tester un hook spécifique
pre-commit run black
pre-commit run pytest

# En urgence (non recommandé)
git commit --no-verify
```

Consultez le [guide de dépannage détaillé](./TROUBLESHOOTING.md) pour plus d'aide.

</details>

---

## 🖥️ Configuration ESP32/ESP8266

<details>
<summary><strong>📦 Dépendances système requises</strong></summary>

```bash
sudo apt update
sudo apt install tmux python3-venv screen
pip install mpfshell
```

> ⚠️ Si `pip` n'est pas installé :
> ```bash
> sudo apt install python3-pip
> ```

</details>

<details>
<summary><strong>🖥️ Utiliser screen pour se connecter à l'ESP32</strong></summary>

**Lister les ports disponibles :**
```bash
ls /dev/ttyUSB*
```

**Se connecter à l'ESP32 :**
```bash
screen /dev/ttyUSB0 115200
```

**Raccourcis utiles dans screen :**
| Action | Raccourci |
|--------|-----------|
| Quitter screen | `Ctrl + A`, puis `K`, puis `Y` |
| Détacher | `Ctrl + A`, puis `D` |
| Revenir | `screen -r` |

</details>

<details>
<summary><strong>🪟 Utiliser tmux pour surveiller plusieurs ESP</strong></summary>

**Lancer tmux :**
```bash
tmux
```

**Diviser l'écran :**
| Action | Raccourci |
|--------|-----------|
| Split horizontal (haut/bas) | `Ctrl + B`, puis `"` |
| Split vertical (gauche/droite) | `Ctrl + B`, puis `%` |
| Naviguer entre panneaux | `Ctrl + B`, puis flèches |
| Activer la souris | `tmux set -g mouse on` |

**Mise en page recommandée :**
```
+-------------------------+-------------------------+
| Terminal série USB0     | Terminal série USB1     |
| (réception)            | (émission)              |
+--------------------------------------------------+
| Terminal libre pour git, mpfshell, etc.         |
+--------------------------------------------------+
```

**Raccourcis tmux :**
| Action | Raccourci |
|--------|-----------|
| Détacher | `Ctrl + B`, puis `D` |
| Rejoindre | `tmux attach` |
| Fermer panneau | `exit` ou `Ctrl + D` |

</details>

---

## 💻 Alternative : Mode simulation PC

**Nouveau !** Vous pouvez maintenant développer et tester sans ESP32 grâce au mode simulation.

📖 **Voir le guide complet :** [Mode simulation PC](./simulation.md)

**Avantages :**
- ✅ Testez votre code sans hardware
- ✅ Débug plus facile avec messages visibles
- ✅ Développement plus rapide

---

## 📚 Liens et ressources

- [Documentation technique du projet](code_explanation.md)
- [Documentation des scripts](scripts.md)
- [Liste des dépendances](dependencies.md) - Liste complète pour réinstallation
- [Mode simulation PC](simulation.md) - Guide détaillé
- [MicroPython REPL docs](https://docs.micropython.org/en/latest/reference/repl.html)
- [tmux Cheat Sheet](https://github.com/rothgar/awesome-tmux)
- [screen User Guide](https://www.gnu.org/software/screen/manual/)

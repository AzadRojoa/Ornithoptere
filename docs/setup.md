
# 🔧 Configuration de l'environnement ESP32 avec tmux, screen, mpfshell, venv

---

## 📦 Dépendances à installer

Ouvre un terminal et exécute :

```bash
sudo apt update
sudo apt install tmux python3-venv screen
pip install mpfshell
```

> ⚠️ Si `pip` n'est pas installé :
> ```bash
> sudo apt install python3-pip
> ```

---

## 🧪 Création de l'environnement virtuel Python

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 🖥️ Utiliser `screen` pour se connecter à l’ESP32

Liste les ports disponibles :
```bash
ls /dev/ttyUSB*
```

Puis connecte-toi à l’ESP32 (remplace le port si besoin) :
```bash
screen /dev/ttyUSB0 115200
```

### 🛑 Raccourcis utiles dans `screen`

| Action                   | Raccourci clavier                 |
|--------------------------|-----------------------------------|
| Quitter `screen`         | `Ctrl + A`, puis `K`, puis `Y`    |
| Détacher (`detach`)      | `Ctrl + A`, puis `D`              |
| Revenir dans `screen`    | `screen -r`                       |

---

## 🪟 Utiliser `tmux` pour spliter l'écran en 3 panneaux

### ▶️ Lancer `tmux`

```bash
tmux
```

### ✂️ Spliter les fenêtres

| Action                            | Raccourci                          |
|-----------------------------------|------------------------------------|
| Split horizontal (haut/bas)       | `Ctrl + B`, puis "%"               |
| Split vertical (gauche/droite)    | `Ctrl + B`, puis "\"              |

> 💡 Tu peux inverser les deux pour ton besoin :
> - `Ctrl + B`, puis `"` → Divise horizontalement (1 ligne en haut, 1 en bas)
> - Sélectionne le **haut**, puis `Ctrl + B`, `%` → Divise verticalement

---

### 🔀 Naviguer entre les panneaux

| Action                               | Raccourci                          |
|--------------------------------------|------------------------------------|
| Changer de panneau                   | `Ctrl + B`, puis flèches (← ↑ ↓ →) |
| Fermer un panneau                    | `exit` ou `Ctrl + D`               |
| Activer la navigation avec la souris | `tmux set -g mouse on`               |


---

### 🛑 Quitter tmux

| Action           | Commande              |
|------------------|-----------------------|
| Détacher         | `Ctrl + B`, puis `D`  |
| Rejoindre        | `tmux attach`         |
| Fermer tous      | `exit` dans chaque panneau ou `Ctrl + D` |

---

## 📁 Exemple de mise en page pour ESP32

```
+-------------------------+-------------------------+
| Terminal série USB0    | Terminal série USB1     |
| (ex: réception)         | (ex: émission)          |
+--------------------------------------------------+
| Terminal libre pour commandes mpfshell, git etc. |
+--------------------------------------------------+
```

---

## 📘 Liens utiles

- [MicroPython REPL docs](https://docs.micropython.org/en/latest/reference/repl.html)
- [tmux Cheat Sheet (GitHub)](https://github.com/rothgar/awesome-tmux)
- [screen User Guide (GNU)](https://www.gnu.org/software/screen/manual/)

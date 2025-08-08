# 🦅 Ornithoptère - Système de Contrôle de Drone à Battement d'Ailes

Un projet de contrôle d'ornithoptère (drone à battement d'ailes) basé sur ESP32 avec communication radio NRF24L01. Le système comprend un émetteur (manette de contrôle) et un récepteur (drone) qui communiquent sans fil.

---

<details>
<summary>🤔 <strong>Qu'est-ce que c'est ?</strong></summary>

Ce projet vous permet de :
- **Contrôler un drone ornithoptère** (qui bat des ailes comme un oiseau) via une manette sans fil
- **Tester le système en simulation** sur votre PC avant de l'utiliser sur le vrai matériel
- **Surveiller en temps réel** les commandes et l'état du système via une interface terminal

**Composants principaux :**
- **Émetteur** : Manette avec joysticks pour envoyer les commandes
- **Récepteur** : Contrôleur de vol qui reçoit les commandes et pilote les moteurs
- **Communication** : Module radio NRF24L01 pour la transmission sans fil

</details>

<details>
<summary>🛠️ <strong>Matériel nécessaire</strong></summary>

### Pour l'émetteur (manette)
- 1× ESP32
- 1× Module NRF24L01
- 2× Joysticks analogiques
- Alimentation (batterie ou USB)

### Pour le récepteur (drone)
- 1× ESP32
- 1× Module NRF24L01
- 2× Moteurs (pour les ailes)
- 2× Servomoteurs (optionnel, pour direction)
- Alimentation (batterie)

### Schéma de branchement
Consultez le fichier `docs/pinout.png` pour le schéma détaillé des connexions.

</details>

<details>
<summary>💻 <strong>Installation</strong></summary>

### 1. Cloner le projet
```bash
git clone <url-du-repo>
cd Ornithoptere
```

### 2. Installation automatique
```bash
# Rendre le script exécutable
chmod +x install.sh

# Lancer l'installation
./install.sh
```

### 3. Installation manuelle (alternative)
```bash
# Installer les dépendances Python
pip install -r requirements.txt

# Pour le développement
pip install -r requirements-dev.txt

# Installer socat (pour la simulation)
sudo apt install socat  # Ubuntu/Debian
# ou
brew install socat      # macOS
```

</details>

<details>
<summary>🔌 <strong>Configuration du matériel</strong></summary>

### Connexions ESP32 - NRF24L01

| ESP32 Pin | NRF24L01 Pin | Description |
|-----------|--------------|-------------|
| 18        | SCK          | Horloge SPI |
| 23        | MOSI         | Données sortie |
| 19        | MISO         | Données entrée |
| 26        | CE           | Chip Enable |
| 27        | CSN          | Chip Select |
| 3.3V      | VCC          | Alimentation |
| GND       | GND          | Masse |

### Connexions joysticks (émetteur)

| Joystick | ESP32 Pins | Description |
|----------|------------|-------------|
| J1       | X:36, Y:39, BTN:32 | Joystick principal |
| J2       | X:33, Y:34, BTN:35 | Joystick secondaire |

### Connexions moteurs (récepteur)

| Composant | ESP32 Pin | Description |
|-----------|-----------|-------------|
| Moteur 1  | 5         | Aile gauche |
| Moteur 2  | (voir code) | Aile droite |

</details>

<details>
<summary>🚀 <strong>Utilisation</strong></summary>

### Mode Simulation (pour débuter)

Le mode simulation vous permet de tester le système sur votre PC sans matériel.

#### Option 1 : Script automatique (recommandé)
```bash
# Lancer la simulation complète
./scripts/start-simu.sh
```

#### Option 2 : Étape par étape
```bash
# Terminal 1 : Créer les ports série virtuels
./simulation_pc/creer_ports_serie.sh

# Terminal 2 : Lancer l'émetteur en simulation
SIMULATION=True python3 source/programme_antenne_emission.py

# Terminal 3 : Lancer le récepteur en simulation
SIMULATION=True python3 source/programme_antenne_reception.py
```

#### Contrôles en simulation
Une fois la simulation lancée, utilisez ces touches dans le terminal émetteur :

| Touche | Action |
|--------|--------|
| `w/s`  | Joystick 1 - Axe Y (haut/bas) |
| `a/d`  | Joystick 1 - Axe X (gauche/droite) |
| `i/k`  | Joystick 2 - Axe Y (haut/bas) |
| `j/l`  | Joystick 2 - Axe X (gauche/droite) |
| `r`    | Reset joysticks au centre |
| `space`| Presser bouton joystick 1 |
| `b`    | Presser bouton joystick 2 |
| `q`    | Quitter |

### Mode Réel (avec ESP32)

#### 1. Préparer le code pour ESP32
Dans les fichiers `programme_antenne_emission.py` et `programme_antenne_reception.py`, changez :
```python
SIMULATION = False  # Mettre à False pour utiliser le matériel réel
```

#### 2. Flasher sur ESP32

**Pour l'émetteur :**
```bash
# Copier le programme émetteur vers ESP32
# (utilisez votre méthode préférée : Thonny, ampy, esptool, etc.)
cp source/programme_antenne_emission.py /path/to/esp32/
cp source/antenne.py /path/to/esp32/
cp source/components.py /path/to/esp32/
cp source/gamepad.py /path/to/esp32/
cp source/nrf24l01.py /path/to/esp32/
```

**Pour le récepteur :**
```bash
# Copier le programme récepteur vers ESP32
cp source/programme_antenne_reception.py /path/to/esp32/
cp source/antenne.py /path/to/esp32/
cp source/components.py /path/to/esp32/
cp source/flight_controler.py /path/to/esp32/
cp source/nrf24l01.py /path/to/esp32/
```

#### 3. Utilisation
1. Alimenter les deux ESP32
2. Le récepteur se met automatiquement en écoute
3. L'émetteur envoie les commandes des joysticks
4. Les moteurs du drone réagissent aux commandes

</details>

<details>
<summary>🔧 <strong>Développement</strong></summary>

### Lancer les tests
```bash
./scripts/run-tests.sh
```

### Vérifier les dépendances
```bash
./scripts/check-dependencies.sh
```

### Configuration pre-commit (optionnel)
```bash
./scripts/setup-precommit.sh
```

### Développer en mode simulation
1. Lancez `./scripts/start-simu.sh`
2. Modifiez le code
3. Relancez les programmes pour tester vos modifications

</details>

<details>
<summary>🔍 <strong>Dépannage</strong></summary>

### Problèmes courants

#### "socat command not found"
```bash
# Installer socat
sudo apt install socat  # Ubuntu/Debian
brew install socat      # macOS
```

#### "Permission denied" sur les ports série
```bash
# Ajouter votre utilisateur au groupe dialout
sudo usermod -a -G dialout $USER
# Puis redémarrer la session
```

#### La communication ne fonctionne pas
1. Vérifiez les connexions matérielles (voir `docs/pinout.png`)
2. Vérifiez que `SIMULATION = False` sur les deux programmes
3. Assurez-vous que les deux ESP32 sont sur le même canal radio

#### Les joysticks ne répondent pas en simulation
1. Vérifiez que le terminal émetteur a le focus
2. Utilisez les bonnes touches (voir tableau des contrôles)
3. Relancez le programme émetteur si nécessaire

### Support

Si vous rencontrez des problèmes :
1. Consultez d'abord cette documentation
2. Vérifiez les logs dans les terminaux
3. Testez d'abord en mode simulation
4. Vérifiez votre matériel avec un multimètre

</details>

---

**Bon vol ! 🚁**

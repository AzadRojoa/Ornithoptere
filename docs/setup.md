# 🔧 Configuration Avancée

Ce guide s'adresse aux développeurs expérimentés qui souhaitent configurer, personnaliser ou contribuer au projet.

## 🛠️ Installation complète

### Environnement de développement

```bash
# Cloner le projet
git clone <votre-repo>/Ornithoptere.git
cd Ornithoptere

# Environnement Python virtuel (recommandé)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Installer toutes les dépendances
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configurer pre-commit (optionnel)
./scripts/setup-precommit.sh
```

### Outils système requis

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install socat minicom screen python3-dev

# macOS
brew install socat minicom screen

# Arch Linux
sudo pacman -S socat minicom screen python
```

## 🔌 Configuration matérielle

### Pinout ESP32 - Émetteur

```python
# Dans programme_antenne_emission.py
inputs = {
    "J1": Joystick(36, 39, 32),  # X, Y, Button
    "J2": Joystick(33, 34, 35),  # X, Y, Button
}

# NRF24L01 connections
# CE  -> GPIO 4
# CSN -> GPIO 5
# SCK -> GPIO 18
# MOSI-> GPIO 23
# MISO-> GPIO 19
# VCC -> 3.3V
# GND -> GND
```

### Pinout ESP32 - Récepteur

```python
# Servomoteurs (exemple)
servo_aile_gauche = ServoMoteur(pin=12)
servo_aile_droite = ServoMoteur(pin=13)
servo_queue = ServoMoteur(pin=14)

# NRF24L01 (même branchement que l'émetteur)
```

### Joysticks analogiques

```
Joystick:
├── VCC -> 3.3V
├── GND -> GND
├── VRx -> GPIO 36 (X axis)
├── VRy -> GPIO 39 (Y axis)
└── SW  -> GPIO 32 (Button)
```

## ⚙️ Configuration avancée

### Paramètres radio NRF24L01

```python
# Dans antenne.py
class Antenne:
    def __init__(self):
        self.channel = 76        # Canal radio (0-125)
        self.power = 3           # Puissance (0-3)
        self.data_rate = 2       # Débit (1=1Mbps, 2=2Mbps)
        self.address = b"Node1"  # Adresse (5 bytes max)
```

### Simulation - Configuration

```python
# Ports série virtuels personnalisés
SIMULATION_PORT_EMETTEUR = "/tmp/custom_emetteur"
SIMULATION_PORT_RECEPTEUR = "/tmp/custom_recepteur"

# Modifier creer_ports_serie.sh en conséquence
socat pty,raw,echo=0,link=/tmp/custom_emetteur pty,raw,echo=0,link=/tmp/custom_recepteur
```

### Contrôle clavier personnalisé

```python
# Dans keyboard_controller.py
self.key_mappings = {
    # Joystick J1 - WASD
    'w': ('J1', 'increment_y', 200),
    's': ('J1', 'increment_y', -200),
    'a': ('J1', 'increment_x', -200),
    'd': ('J1', 'increment_x', 200),

    # Ajouter vos propres mappings
    'q': ('J1', 'increment_y', 50),   # Mouvement fin
    'e': ('J1', 'increment_y', -50),  # Mouvement fin

    # Presets rapides
    '1': ('J1', 'set_preset', 'center'),
    '2': ('J1', 'set_preset', 'full_left'),
}
```

## 🔧 Scripts de développement

### Scripts disponibles

```bash
# Tests
./scripts/run-tests.sh           # Lance tous les tests
./scripts/check-dependencies.sh  # Vérifie les dépendances

# Déploiement
./scripts/deploy.sh              # Déploie sur ESP32
./scripts/start.sh               # Démarre le terminal avec les esp
```

### Script de déploiement personnalisé

```bash
#!/bin/bash
# deploy-custom.sh

ESP32_PORT="/dev/ttyUSB0"  # Adaptez selon votre port
FILES_TO_DEPLOY=(
    "source/programme_antenne_emission.py"
    "source/components.py"
    "source/gamepad.py"
    "source/antenne.py"
    "source/nrf24l01.py"
)

for file in "${FILES_TO_DEPLOY[@]}"; do
    echo "Copie de $file..."
    ampy -p $ESP32_PORT put "$file"
done
```

## 🧪 Tests et validation

### Tests unitaires

```bash
# Tous les tests
python -m pytest source/tests/

# Tests spécifiques
python -m pytest source/tests/test_components.py
python -m pytest source/tests/test_gamepad.py

# Avec couverture
python -m pytest --cov=source source/tests/
```

### Tests d'intégration

```bash
# Test simulation complète
./scripts/start.sh

# Test communication série
python3 benchmark/benchmark_sender.py
python3 benchmark/benchmark_receiver.py
```

### Debugging

```python
# Activer les logs détaillés
import logging
logging.basicConfig(level=logging.DEBUG)

# Logger personnalisé (logger.py)
from logger import Logger
log = Logger("mon_composant")
log.debug("Message de debug")
log.info("Information")
log.error("Erreur")
```

## 🔄 Workflow de développement

### 1. Développement local

```bash
# Mode simulation pour développer
SIMULATION = True

# Tests unitaires
./scripts/run-tests.sh

# Validation manuelle
python3 source/programme_antenne_emission.py
```

### 2. Test sur matériel

```bash
# Déploiement
SIMULATION = False
./scripts/deploy.sh

# Test réel
# Connectez-vous aux ESP32 et testez
```

### 3. Intégration continue

```bash
# Pre-commit hooks
pre-commit install
pre-commit run --all-files

# Format du code
black source/
isort source/

# Linting
flake8 source/
```

## 📊 Monitoring et performance

### Métriques radio

```python
# Dans votre code
def get_radio_stats():
    return {
        "packets_sent": self.packets_sent,
        "packets_lost": self.packets_lost,
        "signal_strength": self.rssi,
        "latency": self.avg_latency
    }
```

### Profiling

```python
import cProfile
import pstats

# Profiler votre code
cProfile.run('votre_fonction()', 'profile.stats')
stats = pstats.Stats('profile.stats')
stats.sort_stats('cumtime').print_stats(10)
```

## 🛡️ Sécurité

### Chiffrement radio (optionnel)

```python
# Ajouter une couche de chiffrement simple
import hashlib

def encrypt_data(data, key):
    # Implémentation basique
    pass

def decrypt_data(data, key):
    # Implémentation basique
    pass
```

### Validation des données

```python
def validate_joystick_data(data):
    """Valide que les données joystick sont cohérentes"""
    for axis in ['x', 'y']:
        if not (0 <= data[axis] <= 4095):
            raise ValueError(f"Valeur {axis} invalide: {data[axis]}")
    return True
```

## 🔌 Extensions possibles

### Nouveaux composants

```python
# Dans components.py
class Accelerometre:
    def __init__(self, i2c_bus):
        self.i2c = i2c_bus

    def read(self):
        # Lecture accéléromètre
        return {"x": 0, "y": 0, "z": 0}

class GPS:
    def __init__(self, uart):
        self.uart = uart

    def get_position(self):
        # Lecture GPS
        return {"lat": 0.0, "lon": 0.0}
```

### Protocoles de communication

```python
# Alternative WiFi
class WiFiAntenne:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password

    def connect(self):
        # Connexion WiFi
        pass

    def send(self, data):
        # Envoi TCP/UDP
        pass
```

---

Cette configuration avancée vous donne toutes les clés pour personnaliser et étendre le projet selon vos besoins spécifiques.

# Ornithoptere

Ce projet permet de piloter un ornithoptère (ou autre dispositif) à l'aide de modules radio NRF24L01 et d'un microcontrôleur compatible MicroPython (ESP32, ESP8266, etc).

---

## 🚀 **DÉMARRAGE ULTRA-RAPIDE**

```bash
git clone [URL_DU_PROJET]
cd Ornithoptere
./install.sh
```

📖 **[Guide complet pour débutants](docs/quickstart.md)**

---

## 📚 Documentation

- **[📖 Index de la documentation](docs/README.md)** ← Commencez ici
- **[🚀 Guide de démarrage rapide](docs/quickstart.md)** ← Pour débuter
- **[🔧 Configuration avancée](docs/setup.md)** ← Pour développeurs
- **[💻 Mode simulation PC](docs/simulation.md)** ← Tester sans ESP32
- **[🛠️ Scripts et outils](docs/scripts.md)** ← Automatisation
- **[🔍 Dépannage](docs/TROUBLESHOOTING.md)** ← Résoudre les problèmes

---

## 🎮 Utilisation rapide

### Mode simulation (recommandé pour débuter)
```bash
source .venv/bin/activate
# Changez SIMULATION = True dans vos programmes .py
./simulation_pc/creer_ports_serie.sh  # Terminal 1
python3 source/programme_antenne_emission.py    # Terminal 2
python3 source/programme_antenne_reception.py   # Terminal 3
```

### Mode ESP32 réel
```bash
source .venv/bin/activate
# Changez SIMULATION = False dans vos programmes .py
./scripts/deploy.sh   # Déployer sur ESP32
./scripts/start.sh    # Surveiller les ESP32
```

---

## 🔌 Schéma de l'ESP32

![Pinout diagram](docs/pinout.png)

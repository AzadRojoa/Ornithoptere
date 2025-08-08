# Architecture du Projet

## 🏗️ Vue d'ensemble

Le projet Ornithoptère suit une architecture modulaire simple avec deux composants principaux communiquant par radio.

```
┌─────────────────┐    Radio NRF24L01    ┌─────────────────┐
│    ÉMETTEUR     │ ◄─────────────────── │    RÉCEPTEUR    │
│                 │                       │                 │
│ ESP32 + Joysticks│                      │ ESP32 + Servos  │
│                 │                       │                 │
│ Lecture inputs  │ ──────────────────► │ Contrôle moteurs│
└─────────────────┘                       └─────────────────┘
```

## 📁 Structure des fichiers

```
Ornithoptere/
├── source/                    # Code principal
│   ├── programme_antenne_emission.py   # Programme émetteur
│   ├── programme_antenne_reception.py  # Programme récepteur
│   ├── components.py          # Composants (Joystick, Servo, etc.)
│   ├── gamepad.py            # Interface gamepad
│   ├── antenne.py            # Communication radio
│   ├── nrf24l01.py          # Driver NRF24L01
│   └── keyboard_controller.py # Contrôle clavier (simulation)
│
├── simulation_pc/            # Outils simulation
│   ├── antenne_serial.py    # Communication série simulée
│   └── creer_ports_serie.sh # Script ports virtuels
│
├── scripts/                 # Scripts utilitaires
├── docs/                   # Documentation
└── tests/                  # Tests et mocks
```

## 🔄 Flux de données

### Mode Normal (ESP32)
1. **Lecture des inputs** - Les joysticks sont lus via ADC
2. **Empaquetage** - Les données sont formatées pour transmission
3. **Transmission radio** - Envoi via NRF24L01
4. **Réception** - Le récepteur decode les données
5. **Action** - Contrôle des servomoteurs/moteurs

### Mode Simulation
1. **Inputs virtuels** - Contrôle clavier remplace les joysticks
2. **Communication série** - Ports virtuels remplacent la radio
3. **Même logique** - Le reste du code reste identique

## 🧩 Composants principaux

### `components.py` - Abstraction matériel
- **Joystick** : Lecture ADC + bouton
- **SimulatedJoystick** : Version simulée pour le développement
- **ServoMoteur** : Contrôle PWM des servos
- **Moteur** : Contrôle PWM des moteurs

### `antenne.py` vs `antenne_serial.py`
- **antenne.py** : Communication radio NRF24L01 (ESP32)
- **antenne_serial.py** : Communication série (simulation PC)
- **Interface identique** : Même API pour les deux modes

### `gamepad.py` - Interface unifiée
- Lit tous les composants d'entrée
- Retourne un dictionnaire unifié
- Fonctionne avec vrais joysticks ou simulés

## 🔀 Modes d'exécution

### 1. Mode Production (ESP32)
```python
SIMULATION = False
# Utilise les vrais composants matériels
# Communication radio NRF24L01
```

### 2. Mode Simulation (PC)
```python
SIMULATION = True
# Utilise des composants simulés
# Communication série virtuelle
# Contrôle clavier activé
```

## 🎯 Avantages de cette architecture

✅ **Modularité** - Chaque composant a une responsabilité claire
✅ **Testabilité** - Simulation complète sans matériel
✅ **Flexibilité** - Facile d'ajouter de nouveaux composants
✅ **Réutilisabilité** - Code réutilisable pour d'autres projets
✅ **Maintenabilité** - Structure claire et documentée

## 🔧 Points d'extension

- **Nouveaux inputs** : Ajouter dans `components.py`
- **Nouveaux outputs** : Ajouter des actuateurs
- **Protocoles radio** : Remplacer `nrf24l01.py`
- **Interface utilisateur** : Modifier `tableau_terminal.py`
- **Logging** : Utiliser `logger.py`

Cette architecture simple mais robuste permet un développement efficace et une maintenance aisée du projet.

# Contrôle Clavier pour la Simulation

## Vue d'ensemble

La fonctionnalité de contrôle clavier permet de simuler les joysticks avec le clavier lorsque le mode simulation est activé (`SIMULATION = True`). Cette fonctionnalité est très pratique pour tester et développer votre code sans avoir besoin du matériel physique.

## Fonctionnalités

### Joysticks Simulés
- **SimulatedJoystick** : Remplace les vrais joysticks en mode simulation
- Valeurs ADC 12 bits (0-4095), centrées par défaut à 2048
- Contrôle précis avec des incréments configurables
- Simulation complète des boutons

### Contrôles Clavier

#### Joystick J1 (Gauche)
- **W** : Augmenter Y (vers le haut)
- **S** : Diminuer Y (vers le bas)
- **A** : Diminuer X (vers la gauche)
- **D** : Augmenter X (vers la droite)
- **ESPACE** : Appuyer sur le bouton
- **R** : Centrer le joystick

#### Joystick J2 (Droite)
- **↑** : Augmenter Y (vers le haut)
- **↓** : Diminuer Y (vers le bas)
- **←** : Diminuer X (vers la gauche)
- **→** : Augmenter X (vers la droite)
- **ENTRÉE** : Appuyer sur le bouton
- **C** : Centrer le joystick

#### Commandes Générales
- **Z** : Centrer tous les joysticks
- **Ctrl+C** : Quitter le programme

## Installation et Configuration

### 1. Activer le Mode Simulation

Dans `programme_antenne_emission.py`, changez :

```python
SIMULATION = True  # Activer la simulation
```

### 2. Démarrer les Ports Série Virtuels

```bash
./simulation_pc/creer_ports_serie.sh
```

Laissez ce script tourner dans un terminal séparé.

### 3. Lancer le Programme

```bash
python3 source/programme_antenne_emission.py
```

## Utilisation

### Interface
Le programme affiche automatiquement :
- L'état des deux joysticks en temps réel
- Les valeurs X, Y pour chaque joystick
- L'état des boutons (🔴 = pressé, ⚪ = relâché)
- Les instructions d'utilisation

### Contrôle Précis
- **Pas d'incrémentation** : 200 unités par défaut
- **Limites** : 0 à 4095 (ADC 12 bits)
- **Centre** : 2048
- **Boutons** : Appui automatiquement relâché après 50ms

### Exemple d'Affichage
```
J1: X=2248 Y=1848 Btn=⚪ | J2: X=2048 Y=2248 Btn=🔴
```

## Architecture Technique

### Classes Principales

#### `SimulatedJoystick`
```python
class SimulatedJoystick:
    def __init__(self, pin_x, pin_y, pin_bt, name="")
    def read() -> Tuple[int, int, int]
    def increment_x(delta: int)
    def increment_y(delta: int)
    def center()
    def press_button()
    def release_button()
```

#### `KeyboardController`
```python
class KeyboardController:
    def __init__(self, joysticks: Dict[str, any])
    def start()  # Démarre dans un thread séparé
    def stop()   # Arrête proprement
    def get_joystick_status() -> str
```

### Intégration
Le système s'intègre automatiquement dans le code existant :

```python
# Mode simulation détecté automatiquement
if SIMULATION:
    inputs = {
        "J1": SimulatedJoystick(36, 39, 32, "J1"),
        "J2": SimulatedJoystick(33, 34, 35, "J2")
    }
    keyboard_controller = KeyboardController(inputs)
    keyboard_controller.start()
else:
    inputs = {"J1": Joystick(36, 39, 32), "J2": Joystick(33, 34, 35)}
```

## Test Rapide

Un script de test rapide est disponible :

```bash
python3 source/test_keyboard.py
```

Ce script teste uniquement le contrôle clavier sans l'interface série.

## Avantages

✅ **Développement Sans Matériel** : Testez votre code sans ESP32
✅ **Contrôle Précis** : Valeurs exactes contrôlables au clavier
✅ **Interface Intuitive** : Contrôles familiers (WASD + flèches)
✅ **Intégration Transparente** : Aucune modification du code principal
✅ **Mode Debug** : Visualisation temps réel des valeurs
✅ **Simulation Complète** : Boutons et joysticks entièrement simulés

## Limitations

⚠️ **Terminal Requis** : Fonctionne uniquement dans un terminal interactif
⚠️ **Une Touche à la Fois** : Pas de combinaisons de touches
⚠️ **Linux/Unix** : Utilise termios (spécifique aux systèmes Unix)

## Dépannage

### Le Contrôleur Clavier ne Répond Pas
- Vérifiez que vous êtes dans un terminal interactif
- Le programme doit être en premier plan
- Essayez le script de test : `python3 source/test_keyboard.py`

### Erreur de Port Série
- Assurez-vous que `./simulation_pc/creer_ports_serie.sh` est en cours d'exécution
- Vérifiez que `socat` est installé : `sudo apt install socat`

### Valeurs qui ne Changent Pas
- Les joysticks sont centrés par défaut (2048)
- Appuyez sur les touches de contrôle pour voir les changements
- Utilisez 'Z' pour recentrer tous les joysticks

---

Cette fonctionnalité rend le développement et les tests beaucoup plus pratiques en permettant une simulation complète du comportement des joysticks directement depuis le clavier !

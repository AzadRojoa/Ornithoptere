import time

# ========== CONFIGURATION SIMULATION ==========
SIMULATION = False  # Changez à True pour utiliser la simulation PC
SIMULATION_PORT_EMETTEUR = "/tmp/esp32_emetteur"
# ===============================================

# Gestion des imports selon le mode
if SIMULATION:
    import os
    import sys

    # Mock du module machine pour la simulation
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tests"))
    from mock_machine import machine

    sys.modules["machine"] = machine

    # Import de l'antenne série pour simulation
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "simulation_pc"))
    from antenne_serial import AntenneSerial as Antenne
else:
    from antenne import Antenne

from components import Bouton, Joystick, SimulatedJoystick
from gamepad import Gamepad
from tableau_terminal import TableauTerminal

# Initialisation des inputs selon le mode
if SIMULATION:
    from keyboard_controller import KeyboardController

    # Utiliser des joysticks simulés en mode simulation
    inputs = {
        "J1": SimulatedJoystick(36, 39, 32, "J1"),
        "J2": SimulatedJoystick(33, 34, 35, "J2"),
    }
else:
    # Utiliser les vrais joysticks sur ESP32
    inputs = {"J1": Joystick(36, 39, 32), "J2": Joystick(33, 34, 35)}

data = {
    "Nom": "emetteur" + (" (SIMULATION)" if SIMULATION else ""),
    "message envoyé": False,
    "Message": "Coucou, ceci est un texte long",
}

# Initialisation de l'antenne selon le mode
if SIMULATION:
    print("🔧 MODE SIMULATION ACTIVÉ")
    print(f"Port série: {SIMULATION_PORT_EMETTEUR}")
    antenne = Antenne(mode="emetteur", port=SIMULATION_PORT_EMETTEUR)

    # Démarrer le contrôleur clavier
    keyboard_controller = KeyboardController(inputs)
    keyboard_controller.start()
else:
    antenne = Antenne(mode="emetteur")
    keyboard_controller = None

gamepad = Gamepad(inputs)
tableau = TableauTerminal(data)
tableau.start()

try:
    while True:
        gamepad_data = gamepad.read()
        data["message envoyé"] = antenne.send(gamepad_data)

        # Ajouter les infos des joysticks simulés à l'affichage
        if SIMULATION and keyboard_controller:
            data["Contrôles"] = keyboard_controller.get_joystick_status()

        tableau.data = data
        time.sleep(0.5)
except KeyboardInterrupt:
    tableau.stop()
    if SIMULATION:
        if keyboard_controller:
            keyboard_controller.stop()
        if hasattr(antenne, "close"):
            antenne.close()
    print("\nArrêt du test.")

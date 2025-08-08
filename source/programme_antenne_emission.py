import time

# ========== CONFIGURATION SIMULATION ==========
SIMULATION = True  # Changez à True pour utiliser la simulation PC
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
    "message envoyé": False,
    "Joystick J1": "",
    "Joystick J2": "",
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
titre_tableau = "emetteur" + (" (SIMULATION)" if SIMULATION else "")
tableau = TableauTerminal(data, titre=titre_tableau)
tableau.start()

try:
    while True:
        gamepad_data = gamepad.read()
        data["message envoyé"] = antenne.send(gamepad_data)

        # Ajouter les infos de chaque joystick séparément à l'affichage
        if SIMULATION and keyboard_controller:
            for name, joystick in keyboard_controller.joysticks.items():
                if (
                    hasattr(joystick, "x")
                    and hasattr(joystick, "y")
                    and hasattr(joystick, "bt")
                ):
                    button_status = "🔴" if joystick.bt == 0 else "⚪"
                    data[
                        f"Joystick {name}"
                    ] = f"X={joystick.x:4d} Y={joystick.y:4d} Btn={button_status}"

        tableau.data = data
        time.sleep(0.1)
except KeyboardInterrupt:
    tableau.stop()
    if SIMULATION:
        if keyboard_controller:
            keyboard_controller.stop()
        if hasattr(antenne, "close"):
            antenne.close()
    print("\nArrêt du test.")

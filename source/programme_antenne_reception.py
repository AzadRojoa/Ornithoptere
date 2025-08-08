from time import sleep

# ========== CONFIGURATION SIMULATION ==========
SIMULATION = True  # Changez à True pour utiliser la simulation PC
SIMULATION_PORT_RECEPTEUR = "/tmp/esp32_recepteur"
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

    # Mock des pins pour simulation
    class MockPin:
        def __init__(self, pin, mode=None):
            self.pin = pin
            self._state = False

        def on(self):
            self._state = True
            # print(f"🟢 PIN {self.pin} ACTIVÉ")

        def off(self):
            self._state = False
            # print(f"🔴 PIN {self.pin} ARRÊTÉ")

    Pin = MockPin
else:
    from antenne import Antenne
    from machine import Pin

from tableau_terminal import TableauTerminal

# Initialisation de l'antenne selon le mode
if SIMULATION:
    print("🔧 MODE SIMULATION ACTIVÉ")
    print(f"Port série: {SIMULATION_PORT_RECEPTEUR}")
    antenne = Antenne(mode="recepteur", port=SIMULATION_PORT_RECEPTEUR)
else:
    antenne = Antenne(mode="recepteur")

moteur1_pin = Pin(5, Pin.OUT if not SIMULATION else None)
moteur2_pin = Pin(17, Pin.OUT if not SIMULATION else None)

# Données pour le tableau
data = {
    "Statut réception": "En attente",
    "Joystick J1": "Pas de données",
    "Joystick J2": "Pas de données",
    "Moteur 1": "Arrêté",
    "Moteur 2": "Arrêté",
}

# Initialisation du tableau
titre_tableau = "récepteur" + (" (SIMULATION)" if SIMULATION else "")
tableau = TableauTerminal(data, titre=titre_tableau)
tableau.start()


def reception_paquets() -> None:
    message = antenne.receive()
    if isinstance(message, dict):
        data["Statut réception"] = "Données reçues ✓"

        # Adaptation pour les nouvelles données (J1, J2 au lieu de X1, Y1, Button1)
        j1_data = message.get("J1")
        if j1_data and len(j1_data) >= 3:
            x, y, btn = j1_data
            button_status = "🔴" if btn == 0 else "⚪"
            data["Joystick J1"] = f"X={x:4d} Y={y:4d} {button_status}"

            if btn == 0:  # Bouton pressé (avec PULL_UP, 0 = pressé)
                moteur1_pin.off()
                moteur2_pin.off()
                data["Moteur 1"] = "Arrêté 🔴"
                data["Moteur 2"] = "Arrêté 🔴"
            else:
                moteur1_pin.on()
                moteur2_pin.on()
                data["Moteur 1"] = "Marche 🟢"
                data["Moteur 2"] = "Marche 🟢"

        # Gestion du J2 si présent
        j2_data = message.get("J2")
        if j2_data and len(j2_data) >= 3:
            x2, y2, btn2 = j2_data
            button_status2 = "🔴" if btn2 == 0 else "⚪"
            data["Joystick J2"] = f"X={x2:4d} Y={y2:4d} {button_status2}"
        else:
            data["Joystick J2"] = "Pas de données"

        # Support de l'ancien format pour compatibilité
        x = message.get("X1")
        y = message.get("Y1")
        btn = message.get("Button1")
        if btn is not None and not j1_data:  # Seulement si pas de données J1
            if btn == 1:
                moteur1_pin.off()
                moteur2_pin.off()
                data["Moteur 1"] = "Arrêté 🔴"
                data["Moteur 2"] = "Arrêté 🔴"
            else:
                moteur1_pin.on()
                moteur2_pin.on()
                data["Moteur 1"] = "Marche 🟢"
                data["Moteur 2"] = "Marche 🟢"
    elif message:
        data["Statut réception"] = f"Données non-dict: {str(message)[:20]}"
    else:
        data["Statut réception"] = "En attente..."

    # Mettre à jour le tableau
    tableau.data = data


try:
    while True:
        reception_paquets()
        if SIMULATION:
            sleep(0.05)  # Plus rapide en simulation
except KeyboardInterrupt:
    tableau.stop()
    if SIMULATION and hasattr(antenne, "close"):
        antenne.close()
    print("\nArrêt de la réception.")

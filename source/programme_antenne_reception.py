from time import sleep

# ========== CONFIGURATION SIMULATION ==========
SIMULATION = False  # Changez à True pour utiliser la simulation PC
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
            print(f"🟢 PIN {self.pin} ACTIVÉ")

        def off(self):
            self._state = False
            print(f"🔴 PIN {self.pin} ARRÊTÉ")

    Pin = MockPin
else:
    from antenne import Antenne
    from machine import Pin

# Initialisation de l'antenne selon le mode
if SIMULATION:
    print("🔧 MODE SIMULATION ACTIVÉ")
    print(f"Port série: {SIMULATION_PORT_RECEPTEUR}")
    antenne = Antenne(mode="recepteur", port=SIMULATION_PORT_RECEPTEUR)
else:
    antenne = Antenne(mode="recepteur")

moteur1_pin = Pin(5, Pin.OUT if not SIMULATION else None)
moteur2_pin = Pin(17, Pin.OUT if not SIMULATION else None)


def reception_paquets() -> None:
    message = antenne.receive()
    if isinstance(message, dict):
        print(f"Données reçues : {message}")

        # Adaptation pour les nouvelles données (J1, J2 au lieu de X1, Y1, Button1)
        j1_data = message.get("J1")
        if j1_data and len(j1_data) >= 3:
            x, y, btn = j1_data
            print(f"Joystick 1: X={x}, Y={y}, Button={btn}")
            if btn == 0:  # Bouton pressé (avec PULL_UP, 0 = pressé)
                print("Demande d'arrêt du moteur")
                moteur1_pin.off()
                moteur2_pin.off()
            else:
                print("Demande de marche du moteur")
                moteur1_pin.on()
                moteur2_pin.on()

        # Support de l'ancien format pour compatibilité
        x = message.get("X1")
        y = message.get("Y1")
        btn = message.get("Button1")
        if btn is not None:
            if btn == 1:
                print("Demande d'arrêt du moteur (ancien format)")
                moteur1_pin.off()
                moteur2_pin.off()
            else:
                print("Demande de marche du moteur (ancien format)")
                moteur1_pin.on()
                moteur2_pin.on()
    elif message:
        print(f"Données reçues non dict : {message}")


try:
    while True:
        reception_paquets()
        if SIMULATION:
            sleep(0.1)  # Plus rapide en simulation
except KeyboardInterrupt:
    if SIMULATION and hasattr(antenne, "close"):
        antenne.close()
    print("\nArrêt de la réception.")

#!/usr/bin/env python3
"""
Test simple du contrôleur clavier sans interface tableau
"""
import os
import sys
import time

# Mock du module machine pour la simulation
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tests"))
from mock_machine import machine

sys.modules["machine"] = machine

from components import SimulatedJoystick
from keyboard_controller import KeyboardController

# Création des joysticks simulés
inputs = {
    "J1": SimulatedJoystick(36, 39, 32, "J1"),
    "J2": SimulatedJoystick(33, 34, 35, "J2"),
}

print("🎮 TEST DU CONTRÔLEUR CLAVIER")
print("=" * 30)

# Démarrer le contrôleur clavier
keyboard_controller = KeyboardController(inputs)
keyboard_controller.start()

try:
    while True:
        # Lire les valeurs des joysticks
        j1_data = inputs["J1"].read()
        j2_data = inputs["J2"].read()

        # Affichage simple
        status = keyboard_controller.get_joystick_status()
        print(f"\r{status}", end="", flush=True)

        time.sleep(0.1)

except KeyboardInterrupt:
    keyboard_controller.stop()
    print("\n\nArrêt du test.")

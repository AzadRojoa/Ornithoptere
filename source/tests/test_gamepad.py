import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import Mock, patch

# Import du mock machine avant les components
from tests.mock_machine import machine

sys.modules["machine"] = machine

from components import Bouton, Joystick, Moteur, ServoMoteur
from gamepad import Gamepad


class TestGamepad(unittest.TestCase):
    def test_read_with_joystick_and_button(self):
        # Création des composants avec les mocks
        joystick = Joystick(pin_x=34, pin_y=35, pin_bt=32)
        bouton = Bouton(pin=25)
        servo = ServoMoteur(pin=18)

        inputs = {"joystick": joystick, "bouton": bouton, "servo": servo}

        gamepad = Gamepad(inputs)
        result = gamepad.read()

        # Vérification que le joystick utilise sa méthode read() (retourne un tuple)
        self.assertIsInstance(result["joystick"], tuple)
        self.assertEqual(len(result["joystick"]), 3)  # x, y, button

        # Vérification que le bouton utilise sa propriété value
        self.assertIsInstance(result["bouton"], int)

        # Vérification que le servo utilise __str__
        self.assertIsInstance(result["servo"], str)
        self.assertIn("ServoMoteur", result["servo"])

    def test_read_with_different_component_types(self):
        # Test avec un joystick (a une méthode read)
        joystick = Joystick(pin_x=34, pin_y=35, pin_bt=32)

        # Test avec un bouton (a une propriété value)
        bouton = Bouton(pin=25)

        # Test avec un moteur (n'a ni read ni value, utilise __str__)
        moteur = Moteur(pin=19)

        inputs = {"stick": joystick, "btn": bouton, "motor": moteur}

        gamepad = Gamepad(inputs)
        result = gamepad.read()

        # Le joystick doit utiliser sa méthode read()
        self.assertIsInstance(result["stick"], tuple)

        # Le bouton doit utiliser sa propriété value
        self.assertIsInstance(result["btn"], int)

        # Le moteur doit utiliser __str__()
        self.assertIsInstance(result["motor"], str)
        self.assertIn("Moteur", result["motor"])

    def test_gamepad_properties_access(self):
        """Test que les propriétés des composants fonctionnent correctement"""
        joystick = Joystick(pin_x=34, pin_y=35, pin_bt=32)
        bouton = Bouton(pin=25)

        # Test des propriétés du joystick
        self.assertIsInstance(joystick.x, int)
        self.assertIsInstance(joystick.y, int)
        self.assertIsInstance(joystick.bt, int)

        # Test des propriétés du bouton
        self.assertIsInstance(bouton.value, int)
        self.assertIsInstance(bouton.is_pressed(), bool)


if __name__ == "__main__":
    unittest.main()

"""
Tests unitaires simplifiés pour le module Joystick
"""
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# IMPORTANT: Importer les mocks MicroPython AVANT tout autre import
from tests.micropython_mocks import setup_micropython_mocks
setup_micropython_mocks()

import unittest
from source.joystick import Joystick

class TestJoystick(unittest.TestCase):
    
    def test_init_default(self):
        """Test l'initialisation avec les paramètres par défaut"""
        joystick = Joystick(34, 35, 32)
        self.assertIsNotNone(joystick._x)
        self.assertIsNotNone(joystick._y)
        self.assertIsNotNone(joystick._bt)
    
    def test_x_property(self):
        """Test la propriété x"""
        joystick = Joystick(34, 35, 32)
        joystick._x._value = 1000
        self.assertEqual(joystick.x, 1000)
        
        joystick._x._value = 3000
        self.assertEqual(joystick.x, 3000)
    
    def test_y_property(self):
        """Test la propriété y"""
        joystick = Joystick(34, 35, 32)
        joystick._y._value = 500
        self.assertEqual(joystick.y, 500)
        
        joystick._y._value = 4000
        self.assertEqual(joystick.y, 4000)
    
    def test_bt_property(self):
        """Test la propriété bt (bouton)"""
        joystick = Joystick(34, 35, 32)
        
        joystick._bt._value = 1
        self.assertEqual(joystick.bt, 1)
        
        joystick._bt._value = 0
        self.assertEqual(joystick.bt, 0)
    
    def test_read_method(self):
        """Test la méthode read"""
        joystick = Joystick(34, 35, 32)
        
        joystick._x._value = 1500
        joystick._y._value = 2500
        joystick._bt._value = 0
        
        result = joystick.read()
        self.assertEqual(result, (1500, 2500, 0))
    
    def test_str_method(self):
        """Test la méthode __str__"""
        joystick = Joystick(34, 35, 32)
        
        joystick._x._value = 1200
        joystick._y._value = 3400
        joystick._bt._value = 1
        
        expected = "Joystick(X=1200, Y=3400, Button=1)"
        self.assertEqual(str(joystick), expected)

if __name__ == '__main__':
    unittest.main()

"""
Tests unitaires pour le module Bouton
"""
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# IMPORTANT: Importer les mocks MicroPython AVANT tout autre import
from tests.micropython_mocks import setup_micropython_mocks
setup_micropython_mocks()

import unittest
from unittest.mock import patch, MagicMock
from source.bouton import Bouton

class TestBouton(unittest.TestCase):
    
    def test_init_default(self):
        """Test l'initialisation avec les paramètres par défaut"""
        bouton = Bouton(5)
        self.assertIsNotNone(bouton._pin)
        
    def test_init_custom_pull(self):
        """Test l'initialisation avec un pull personnalisé"""
        from machine import Pin
        bouton = Bouton(5, Pin.PULL_DOWN)
        self.assertIsNotNone(bouton._pin)
    
    def test_is_pressed_true(self):
        """Test is_pressed quand le bouton est pressé (valeur 0)"""
        bouton = Bouton(5)
        bouton._pin._value = 0
        
        self.assertTrue(bouton.is_pressed())
    
    def test_is_pressed_false(self):
        """Test is_pressed quand le bouton n'est pas pressé (valeur 1)"""
        bouton = Bouton(5)
        bouton._pin._value = 1
        
        self.assertFalse(bouton.is_pressed())
    
    def test_value_property(self):
        """Test la propriété value"""
        bouton = Bouton(5)
        
        bouton._pin._value = 1
        self.assertEqual(bouton.value, 1)
        
        bouton._pin._value = 0
        self.assertEqual(bouton.value, 0)
    
    def test_pin_property(self):
        """Test la propriété pin"""
        bouton = Bouton(5)
        self.assertEqual(bouton.pin, 5)
    
    def test_str_method(self):
        """Test la méthode __str__"""
        bouton = Bouton(5)
        bouton._pin._value = 1
        
        expected = "Bouton(pin=5, value=1)"
        self.assertEqual(str(bouton), expected)

if __name__ == '__main__':
    unittest.main()

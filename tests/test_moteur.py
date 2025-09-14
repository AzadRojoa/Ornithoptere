"""
Tests unitaires pour le module Moteur
"""
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# IMPORTANT: Importer les mocks MicroPython AVANT tout autre import
from tests.micropython_mocks import setup_micropython_mocks
setup_micropython_mocks()

import unittest
from source.moteur import Moteur

class TestMoteur(unittest.TestCase):
    
    def test_init_default_freq(self):
        """Test l'initialisation avec la fréquence par défaut"""
        moteur = Moteur(13)
        self.assertIsNotNone(moteur.pwm)
        self.assertEqual(moteur._duty, 512)
    
    def test_init_custom_freq(self):
        """Test l'initialisation avec une fréquence personnalisée"""
        moteur = Moteur(13, 2000)
        self.assertIsNotNone(moteur.pwm)
    
    def test_set_speed(self):
        """Test la méthode set_speed"""
        moteur = Moteur(13)
        
        # Test avec 50%
        moteur.set_speed(50)
        self.assertEqual(moteur._duty, 511)  # 50 * 1023 / 100 = 511.5 -> 511
        
        # Test avec 100%
        moteur.set_speed(100)
        self.assertEqual(moteur._duty, 1023)
        
        # Test avec 0%
        moteur.set_speed(0)
        self.assertEqual(moteur._duty, 0)
    
    def test_duty_property_getter(self):
        """Test le getter de la propriété duty"""
        moteur = Moteur(13)
        moteur._duty = 800
        self.assertEqual(moteur.duty, 800)
    
    def test_duty_property_setter(self):
        """Test le setter de la propriété duty"""
        moteur = Moteur(13)
        moteur.duty = 75
        self.assertEqual(moteur._duty, 767)  # 75 * 1023 / 100 = 767.25 -> 767
    
    def test_frequency_property_getter(self):
        """Test le getter de la propriété frequency"""
        moteur = Moteur(13, 1500)
        self.assertEqual(moteur.frequency, 1500)
    
    def test_frequency_property_setter(self):
        """Test le setter de la propriété frequency"""
        moteur = Moteur(13)
        moteur.frequency = 2500
        self.assertEqual(moteur.pwm._freq, 2500)
    
    def test_speed_property_getter(self):
        """Test le getter de la propriété speed"""
        moteur = Moteur(13)
        
        moteur._duty = 511  # ~50%
        self.assertEqual(moteur.speed, 49)  # 511 * 100 / 1023 = 49.95 -> 49
        
        moteur._duty = 1023  # 100%
        self.assertEqual(moteur.speed, 100)
        
        moteur._duty = 0  # 0%
        self.assertEqual(moteur.speed, 0)
    
    def test_speed_property_setter(self):
        """Test le setter de la propriété speed"""
        moteur = Moteur(13)
        
        moteur.speed = 25
        self.assertEqual(moteur._duty, 255)  # 25 * 1023 / 100 = 255.75 -> 255
        
        moteur.speed = 80
        self.assertEqual(moteur._duty, 818)  # 80 * 1023 / 100 = 818.4 -> 818

if __name__ == '__main__':
    unittest.main()

"""
Tests unitaires pour le module ServoMoteur
"""
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# IMPORTANT: Importer les mocks MicroPython AVANT tout autre import
from tests.micropython_mocks import setup_micropython_mocks
setup_micropython_mocks()

import unittest
from source.servomoteurs import ServoMoteur

class TestServoMoteur(unittest.TestCase):
    
    def test_init_default_params(self):
        """Test l'initialisation avec les paramètres par défaut"""
        servo = ServoMoteur(9)
        
        self.assertIsNotNone(servo.pwm)
        self.assertEqual(servo.min_us, 500)
        self.assertEqual(servo.max_us, 2500)
        self.assertEqual(servo._angle, 0)
    
    def test_init_custom_params(self):
        """Test l'initialisation avec des paramètres personnalisés"""
        servo = ServoMoteur(9, freq=60, min_us=1000, max_us=2000)
        
        self.assertEqual(servo.min_us, 1000)
        self.assertEqual(servo.max_us, 2000)
    
    def test_angle_method_0_degrees(self):
        """Test la méthode angle avec 0 degrés"""
        servo = ServoMoteur(9)
        servo.angle(0)
        
        # Calcul attendu: us = 500 + (2500 - 500) * 0 / 180 = 500
        # duty = 500 * 1023 / 20000 = 25.575 -> 25
        self.assertEqual(servo._angle, 0)
        self.assertEqual(servo.pwm._duty, 25)
    
    def test_angle_method_90_degrees(self):
        """Test la méthode angle avec 90 degrés"""
        servo = ServoMoteur(9)
        servo.angle(90)
        
        # Calcul attendu: us = 500 + (2500 - 500) * 90 / 180 = 1500
        # duty = 1500 * 1023 / 20000 = 76.725 -> 76
        self.assertEqual(servo._angle, 90)
        self.assertEqual(servo.pwm._duty, 76)
    
    def test_angle_method_180_degrees(self):
        """Test la méthode angle avec 180 degrés"""
        servo = ServoMoteur(9)
        servo.angle(180)
        
        # Calcul attendu: us = 500 + (2500 - 500) * 180 / 180 = 2500
        # duty = 2500 * 1023 / 20000 = 127.875 -> 127
        self.assertEqual(servo._angle, 180)
        self.assertEqual(servo.pwm._duty, 127)
    
    def test_frequency_property_getter(self):
        """Test le getter de la propriété frequency"""
        servo = ServoMoteur(9, freq=60)
        self.assertEqual(servo.frequency, 60)
    
    def test_frequency_property_setter(self):
        """Test le setter de la propriété frequency"""
        servo = ServoMoteur(9)
        servo.frequency = 100
        self.assertEqual(servo.pwm._freq, 100)
    
    def test_deg_property_getter(self):
        """Test le getter de la propriété deg"""
        servo = ServoMoteur(9)
        servo._angle = 45
        self.assertEqual(servo.deg, 45)
    
    def test_deg_property_setter(self):
        """Test le setter de la propriété deg"""
        servo = ServoMoteur(9)
        servo.deg = 120
        
        # Vérifier que la méthode angle a été appelée correctement
        self.assertEqual(servo._angle, 120)
        # Calcul attendu: us = 500 + (2500 - 500) * 120 / 180 = 1833
        # duty = 1833 * 1023 / 20000 = 93.81 -> 93
        self.assertEqual(servo.pwm._duty, 93)
    
    def test_custom_range_servo(self):
        """Test avec une plage personnalisée de microsecondes"""
        servo = ServoMoteur(9, min_us=1000, max_us=2000)
        servo.angle(90)
        
        # Calcul attendu: us = 1000 + (2000 - 1000) * 90 / 180 = 1500
        # duty = 1500 * 1023 / 20000 = 76.725 -> 76
        self.assertEqual(servo._angle, 90)
        self.assertEqual(servo.pwm._duty, 76)

if __name__ == '__main__':
    unittest.main()

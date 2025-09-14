"""
Tests unitaires pour le module Moteur
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Ajouter le répertoire source au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from tests.mocks import MockPin, MockPWM

class TestMoteur(unittest.TestCase):
    
    def setUp(self):
        """Setup pour chaque test"""
        self.mock_pin = MockPin(pin_id=13, mode=MockPin.OUT)
        self.mock_pwm = MockPWM(self.mock_pin, freq=1000)
        
    @patch('moteur.PWM')
    @patch('moteur.Pin')
    def test_init_default_freq(self, mock_pin_class, mock_pwm_class):
        """Test l'initialisation avec la fréquence par défaut"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from moteur import Moteur
        moteur = Moteur(13)
        
        mock_pin_class.assert_called_once_with(13)
        mock_pwm_class.assert_called_once_with(self.mock_pin, freq=1000)
        self.assertEqual(moteur._duty, 512)
    
    @patch('moteur.PWM')
    @patch('moteur.Pin')
    def test_init_custom_freq(self, mock_pin_class, mock_pwm_class):
        """Test l'initialisation avec une fréquence personnalisée"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from moteur import Moteur
        moteur = Moteur(13, 2000)
        
        mock_pwm_class.assert_called_once_with(self.mock_pin, freq=2000)
    
    @patch('moteur.PWM')
    @patch('moteur.Pin')
    def test_set_speed(self, mock_pin_class, mock_pwm_class):
        """Test la méthode set_speed"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from moteur import Moteur
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
    
    @patch('moteur.PWM')
    @patch('moteur.Pin')
    def test_duty_property_getter(self, mock_pin_class, mock_pwm_class):
        """Test le getter de la propriété duty"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from moteur import Moteur
        moteur = Moteur(13)
        
        moteur._duty = 800
        self.assertEqual(moteur.duty, 800)
    
    @patch('moteur.PWM')
    @patch('moteur.Pin')
    def test_duty_property_setter(self, mock_pin_class, mock_pwm_class):
        """Test le setter de la propriété duty"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from moteur import Moteur
        moteur = Moteur(13)
        
        moteur.duty = 75
        self.assertEqual(moteur._duty, 766)  # 75 * 1023 / 100 = 767.25 -> 767
    
    @patch('moteur.PWM')
    @patch('moteur.Pin')
    def test_frequency_property_getter(self, mock_pin_class, mock_pwm_class):
        """Test le getter de la propriété frequency"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from moteur import Moteur
        moteur = Moteur(13, 1500)
        
        self.mock_pwm._freq = 1500
        self.assertEqual(moteur.frequency, 1500)
    
    @patch('moteur.PWM')
    @patch('moteur.Pin')
    def test_frequency_property_setter(self, mock_pin_class, mock_pwm_class):
        """Test le setter de la propriété frequency"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from moteur import Moteur
        moteur = Moteur(13)
        
        moteur.frequency = 2500
        self.assertEqual(self.mock_pwm._freq, 2500)
    
    @patch('moteur.PWM')
    @patch('moteur.Pin')
    def test_speed_property_getter(self, mock_pin_class, mock_pwm_class):
        """Test le getter de la propriété speed"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from moteur import Moteur
        moteur = Moteur(13)
        
        moteur._duty = 511  # ~50%
        self.assertEqual(moteur.speed, 49)  # 511 * 100 / 1023 = 49.95 -> 49
        
        moteur._duty = 1023  # 100%
        self.assertEqual(moteur.speed, 100)
        
        moteur._duty = 0  # 0%
        self.assertEqual(moteur.speed, 0)
    
    @patch('moteur.PWM')
    @patch('moteur.Pin')
    def test_speed_property_setter(self, mock_pin_class, mock_pwm_class):
        """Test le setter de la propriété speed"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from moteur import Moteur
        moteur = Moteur(13)
        
        moteur.speed = 25
        self.assertEqual(moteur._duty, 255)  # 25 * 1023 / 100 = 255.75 -> 255
        
        moteur.speed = 80
        self.assertEqual(moteur._duty, 818)  # 80 * 1023 / 100 = 818.4 -> 818

if __name__ == '__main__':
    unittest.main()

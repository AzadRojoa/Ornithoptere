"""
Tests unitaires pour le module ServoMoteur
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Ajouter le répertoire source au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from tests.mocks import MockPin, MockPWM

class TestServoMoteur(unittest.TestCase):
    
    def setUp(self):
        """Setup pour chaque test"""
        self.mock_pin = MockPin(pin_id=9, mode=MockPin.OUT)
        self.mock_pwm = MockPWM(self.mock_pin, freq=50)
        
    @patch('servomoteurs.PWM')
    @patch('servomoteurs.Pin')
    def test_init_default_params(self, mock_pin_class, mock_pwm_class):
        """Test l'initialisation avec les paramètres par défaut"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from servomoteurs import ServoMoteur
        servo = ServoMoteur(9)
        
        mock_pin_class.assert_called_once_with(9)
        mock_pwm_class.assert_called_once_with(self.mock_pin, freq=50)
        self.assertEqual(servo.min_us, 500)
        self.assertEqual(servo.max_us, 2500)
        self.assertEqual(servo._angle, 0)
    
    @patch('servomoteurs.PWM')
    @patch('servomoteurs.Pin')
    def test_init_custom_params(self, mock_pin_class, mock_pwm_class):
        """Test l'initialisation avec des paramètres personnalisés"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from servomoteurs import ServoMoteur
        servo = ServoMoteur(9, freq=60, min_us=1000, max_us=2000)
        
        mock_pwm_class.assert_called_once_with(self.mock_pin, freq=60)
        self.assertEqual(servo.min_us, 1000)
        self.assertEqual(servo.max_us, 2000)
    
    @patch('servomoteurs.PWM')
    @patch('servomoteurs.Pin')
    def test_angle_method_0_degrees(self, mock_pin_class, mock_pwm_class):
        """Test la méthode angle avec 0 degrés"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from servomoteurs import ServoMoteur
        servo = ServoMoteur(9)
        
        servo.angle(0)
        
        # Calcul attendu: us = 500 + (2500 - 500) * 0 / 180 = 500
        # duty = 500 * 1023 / 20000 = 25.575 -> 25
        self.assertEqual(servo._angle, 0)
        self.assertEqual(self.mock_pwm._duty, 25)
    
    @patch('servomoteurs.PWM')
    @patch('servomoteurs.Pin')
    def test_angle_method_90_degrees(self, mock_pin_class, mock_pwm_class):
        """Test la méthode angle avec 90 degrés"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from servomoteurs import ServoMoteur
        servo = ServoMoteur(9)
        
        servo.angle(90)
        
        # Calcul attendu: us = 500 + (2500 - 500) * 90 / 180 = 1500
        # duty = 1500 * 1023 / 20000 = 76.725 -> 76
        self.assertEqual(servo._angle, 90)
        self.assertEqual(self.mock_pwm._duty, 76)
    
    @patch('servomoteurs.PWM')
    @patch('servomoteurs.Pin')
    def test_angle_method_180_degrees(self, mock_pin_class, mock_pwm_class):
        """Test la méthode angle avec 180 degrés"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from servomoteurs import ServoMoteur
        servo = ServoMoteur(9)
        
        servo.angle(180)
        
        # Calcul attendu: us = 500 + (2500 - 500) * 180 / 180 = 2500
        # duty = 2500 * 1023 / 20000 = 127.875 -> 127
        self.assertEqual(servo._angle, 180)
        self.assertEqual(self.mock_pwm._duty, 127)
    
    @patch('servomoteurs.PWM')
    @patch('servomoteurs.Pin')
    def test_frequency_property_getter(self, mock_pin_class, mock_pwm_class):
        """Test le getter de la propriété frequency"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from servomoteurs import ServoMoteur
        servo = ServoMoteur(9, freq=60)
        
        self.mock_pwm._freq = 60
        self.assertEqual(servo.frequency, 60)
    
    @patch('servomoteurs.PWM')
    @patch('servomoteurs.Pin')
    def test_frequency_property_setter(self, mock_pin_class, mock_pwm_class):
        """Test le setter de la propriété frequency"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from servomoteurs import ServoMoteur
        servo = ServoMoteur(9)
        
        servo.frequency = 100
        self.assertEqual(self.mock_pwm._freq, 100)
    
    @patch('servomoteurs.PWM')
    @patch('servomoteurs.Pin')
    def test_deg_property_getter(self, mock_pin_class, mock_pwm_class):
        """Test le getter de la propriété deg"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from servomoteurs import ServoMoteur
        servo = ServoMoteur(9)
        
        servo._angle = 45
        self.assertEqual(servo.deg, 45)
    
    @patch('servomoteurs.PWM')
    @patch('servomoteurs.Pin')
    def test_deg_property_setter(self, mock_pin_class, mock_pwm_class):
        """Test le setter de la propriété deg"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from servomoteurs import ServoMoteur
        servo = ServoMoteur(9)
        
        servo.deg = 120
        
        # Vérifier que la méthode angle a été appelée correctement
        self.assertEqual(servo._angle, 120)
        # Calcul attendu: us = 500 + (2500 - 500) * 120 / 180 = 1833
        # duty = 1833 * 1023 / 20000 = 93.81 -> 93
        self.assertEqual(self.mock_pwm._duty, 93)
    
    @patch('servomoteurs.PWM')
    @patch('servomoteurs.Pin')
    def test_custom_range_servo(self, mock_pin_class, mock_pwm_class):
        """Test avec une plage personnalisée de microsecondes"""
        mock_pin_class.return_value = self.mock_pin
        mock_pwm_class.return_value = self.mock_pwm
        
        from servomoteurs import ServoMoteur
        servo = ServoMoteur(9, min_us=1000, max_us=2000)
        
        servo.angle(90)
        
        # Calcul attendu: us = 1000 + (2000 - 1000) * 90 / 180 = 1500
        # duty = 1500 * 1023 / 20000 = 76.725 -> 76
        self.assertEqual(servo._angle, 90)
        self.assertEqual(self.mock_pwm._duty, 76)

if __name__ == '__main__':
    unittest.main()

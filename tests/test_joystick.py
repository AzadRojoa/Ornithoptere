"""
Tests unitaires pour le module Joystick
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Ajouter le répertoire source au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from tests.mocks import MockPin, MockADC

class TestJoystick(unittest.TestCase):
    
    def setUp(self):
        """Setup pour chaque test"""
        self.mock_pin_x = MockPin(34)
        self.mock_pin_y = MockPin(35)
        self.mock_pin_bt = MockPin(32, MockPin.IN, MockPin.PULL_UP)
        
        self.mock_adc_x = MockADC(self.mock_pin_x)
        self.mock_adc_y = MockADC(self.mock_pin_y)
        
        # Valeurs par défaut
        self.mock_adc_x.set_value(2048)
        self.mock_adc_y.set_value(2048)
        self.mock_pin_bt._value = 1
        
    @patch('joystick.Pin')
    @patch('joystick.ADC')
    def test_init_default(self, mock_adc_class, mock_pin_class):
        """Test l'initialisation avec les paramètres par défaut"""
        mock_pin_class.side_effect = [self.mock_pin_x, self.mock_pin_y, self.mock_pin_bt]
        mock_adc_class.side_effect = [self.mock_adc_x, self.mock_adc_y]
        
        from joystick import Joystick
        joystick = Joystick(34, 35, 32)
        
        # Vérifier les appels
        self.assertEqual(mock_pin_class.call_count, 3)
        self.assertEqual(mock_adc_class.call_count, 2)
    
    @patch('joystick.Pin')
    @patch('joystick.ADC')
    def test_init_custom_attenuation(self, mock_adc_class, mock_pin_class):
        """Test l'initialisation avec une atténuation personnalisée"""
        mock_pin_class.side_effect = [self.mock_pin_x, self.mock_pin_y, self.mock_pin_bt]
        mock_adc_class.side_effect = [self.mock_adc_x, self.mock_adc_y]
        
        from joystick import Joystick
        joystick = Joystick(34, 35, 32, MockADC.ATTN_11DB)
        
        # Les ADC doivent avoir été configurés avec l'atténuation
        self.assertEqual(mock_adc_class.call_count, 2)
    
    @patch('joystick.Pin')
    @patch('joystick.ADC')
    def test_x_property(self, mock_adc_class, mock_pin_class):
        """Test la propriété x"""
        mock_pin_class.side_effect = [self.mock_pin_x, self.mock_pin_y, self.mock_pin_bt]
        mock_adc_class.side_effect = [self.mock_adc_x, self.mock_adc_y]
        
        from joystick import Joystick
        joystick = Joystick(34, 35, 32)
        
        self.mock_adc_x.set_value(1000)
        self.assertEqual(joystick.x, 1000)
        
        self.mock_adc_x.set_value(3000)
        self.assertEqual(joystick.x, 3000)
    
    @patch('joystick.Pin')
    @patch('joystick.ADC')
    def test_y_property(self, mock_adc_class, mock_pin_class):
        """Test la propriété y"""
        mock_pin_class.side_effect = [self.mock_pin_x, self.mock_pin_y, self.mock_pin_bt]
        mock_adc_class.side_effect = [self.mock_adc_x, self.mock_adc_y]
        
        from joystick import Joystick
        joystick = Joystick(34, 35, 32)
        
        self.mock_adc_y.set_value(500)
        self.assertEqual(joystick.y, 500)
        
        self.mock_adc_y.set_value(4000)
        self.assertEqual(joystick.y, 4000)
    
    @patch('joystick.Pin')
    @patch('joystick.ADC')
    def test_bt_property(self, mock_adc_class, mock_pin_class):
        """Test la propriété bt (bouton)"""
        mock_pin_class.side_effect = [self.mock_pin_x, self.mock_pin_y, self.mock_pin_bt]
        mock_adc_class.side_effect = [self.mock_adc_x, self.mock_adc_y]
        
        from joystick import Joystick
        joystick = Joystick(34, 35, 32)
        
        self.mock_pin_bt._value = 1
        self.assertEqual(joystick.bt, 1)
        
        self.mock_pin_bt._value = 0
        self.assertEqual(joystick.bt, 0)
    
    @patch('joystick.Pin')
    @patch('joystick.ADC')
    def test_read_method(self, mock_adc_class, mock_pin_class):
        """Test la méthode read"""
        mock_pin_class.side_effect = [self.mock_pin_x, self.mock_pin_y, self.mock_pin_bt]
        mock_adc_class.side_effect = [self.mock_adc_x, self.mock_adc_y]
        
        from joystick import Joystick
        joystick = Joystick(34, 35, 32)
        
        self.mock_adc_x.set_value(1500)
        self.mock_adc_y.set_value(2500)
        self.mock_pin_bt._value = 0
        
        result = joystick.read()
        self.assertEqual(result, (1500, 2500, 0))
    
    @patch('joystick.Pin')
    @patch('joystick.ADC')
    def test_str_method(self, mock_adc_class, mock_pin_class):
        """Test la méthode __str__"""
        mock_pin_class.side_effect = [self.mock_pin_x, self.mock_pin_y, self.mock_pin_bt]
        mock_adc_class.side_effect = [self.mock_adc_x, self.mock_adc_y]
        
        from joystick import Joystick
        joystick = Joystick(34, 35, 32)
        
        self.mock_adc_x.set_value(1200)
        self.mock_adc_y.set_value(3400)
        self.mock_pin_bt._value = 1
        
        expected = "Joystick(X=1200, Y=3400, Button=1)"
        self.assertEqual(str(joystick), expected)

if __name__ == '__main__':
    unittest.main()

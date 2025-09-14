"""
Tests unitaires pour le module Antenne
"""
import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Ajouter le répertoire source au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source'))

from tests.mocks import MockPin, MockSPI, MockNRF24L01

class TestAntenne(unittest.TestCase):
    
    def setUp(self):
        """Setup pour chaque test"""
        self.mock_spi = MockSPI(1)
        self.mock_ce = MockPin(26, MockPin.OUT)
        self.mock_csn = MockPin(27, MockPin.OUT)
        self.mock_nrf = MockNRF24L01(self.mock_spi, self.mock_csn, self.mock_ce)
        
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_init_emetteur_mode(self, mock_spi_class, mock_pin_class, mock_nrf_class):
        """Test l'initialisation en mode émetteur"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        
        from antenne import Antenne
        antenne = Antenne(mode='emetteur')
        
        self.assertEqual(antenne.mode, 'emetteur')
        self.assertEqual(antenne._address, b"2Node")
        self.assertEqual(antenne._channel, 76)
        self.assertEqual(antenne._payload_size, 32)
    
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_init_recepteur_mode(self, mock_spi_class, mock_pin_class, mock_nrf_class):
        """Test l'initialisation en mode récepteur"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        
        from antenne import Antenne
        antenne = Antenne(mode='recepteur')
        
        self.assertEqual(antenne.mode, 'recepteur')
    
    def test_init_invalid_mode(self):
        """Test l'initialisation avec un mode invalide"""
        from antenne import Antenne
        
        with self.assertRaises(ValueError) as context:
            Antenne(mode='invalid')
        
        self.assertIn("mode must be 'emetteur' or 'recepteur'", str(context.exception))
    
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_send_string_success(self, mock_spi_class, mock_pin_class, mock_nrf_class):
        """Test l'envoi d'un message string avec succès"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        
        from antenne import Antenne
        antenne = Antenne(mode='emetteur')
        
        result = antenne.send("Hello World")
        
        self.assertTrue(result)
    
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_send_bytes_success(self, mock_spi_class, mock_pin_class, mock_nrf_class):
        """Test l'envoi d'un message bytes avec succès"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        
        from antenne import Antenne
        antenne = Antenne(mode='emetteur')
        
        result = antenne.send(b"Hello Bytes")
        
        self.assertTrue(result)
    
    @patch('antenne.ujson.dumps')
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_send_dict_success(self, mock_spi_class, mock_pin_class, mock_nrf_class, mock_json_dumps):
        """Test l'envoi d'un dictionnaire avec succès"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        mock_json_dumps.return_value = '{"test": "value"}'
        
        from antenne import Antenne
        antenne = Antenne(mode='emetteur')
        
        test_dict = {"test": "value"}
        result = antenne.send(test_dict)
        
        self.assertTrue(result)
        mock_json_dumps.assert_called_once_with(test_dict)
    
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_send_failure(self, mock_spi_class, mock_pin_class, mock_nrf_class):
        """Test l'envoi avec échec (OSError)"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        
        # Configure le mock pour lever une OSError
        self.mock_nrf.send = MagicMock(side_effect=OSError("No ACK"))
        
        from antenne import Antenne
        antenne = Antenne(mode='emetteur')
        
        result = antenne.send("Hello World")
        
        self.assertFalse(result)
    
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_send_in_recepteur_mode(self, mock_spi_class, mock_pin_class, mock_nrf_class):
        """Test l'envoi en mode récepteur (doit lever une exception)"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        
        from antenne import Antenne
        antenne = Antenne(mode='recepteur')
        
        with self.assertRaises(RuntimeError) as context:
            antenne.send("Hello")
        
        self.assertIn("Cannot send in recepteur mode", str(context.exception))
    
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_receive_string_message(self, mock_spi_class, mock_pin_class, mock_nrf_class):
        """Test la réception d'un message string"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        
        from antenne import Antenne
        antenne = Antenne(mode='recepteur')
        
        # Ajouter un message au mock
        self.mock_nrf.add_message(b"Hello World")
        
        result = antenne.receive()
        
        self.assertEqual(result, "Hello World")
    
    @patch('antenne.ujson.loads')
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_receive_json_message(self, mock_spi_class, mock_pin_class, mock_nrf_class, mock_json_loads):
        """Test la réception d'un message JSON"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        mock_json_loads.return_value = {"test": "value"}
        
        from antenne import Antenne
        antenne = Antenne(mode='recepteur')
        
        # Ajouter un message JSON au mock (commence par 'J')
        self.mock_nrf.add_message(b'J{"test": "value"}')
        
        result = antenne.receive()
        
        self.assertEqual(result, {"test": "value"})
        mock_json_loads.assert_called_once_with('{"test": "value"}')
    
    @patch('antenne.ujson.loads')
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_receive_invalid_json(self, mock_spi_class, mock_pin_class, mock_nrf_class, mock_json_loads):
        """Test la réception d'un JSON invalide"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        mock_json_loads.side_effect = ValueError("Invalid JSON")
        
        from antenne import Antenne
        antenne = Antenne(mode='recepteur')
        
        # Ajouter un message JSON invalide au mock
        self.mock_nrf.add_message(b'J{invalid json}')
        
        result = antenne.receive()
        
        self.assertIsNone(result)
    
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_receive_no_message(self, mock_spi_class, mock_pin_class, mock_nrf_class):
        """Test la réception quand il n'y a pas de message"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        
        from antenne import Antenne
        antenne = Antenne(mode='recepteur')
        
        result = antenne.receive()
        
        self.assertIsNone(result)
    
    @patch('antenne.NRF24L01')
    @patch('antenne.Pin')
    @patch('antenne.SPI')
    def test_receive_in_emetteur_mode(self, mock_spi_class, mock_pin_class, mock_nrf_class):
        """Test la réception en mode émetteur (doit lever une exception)"""
        mock_spi_class.return_value = self.mock_spi
        mock_pin_class.side_effect = [MockPin(18), MockPin(23), MockPin(19), self.mock_ce, self.mock_csn]
        mock_nrf_class.return_value = self.mock_nrf
        
        from antenne import Antenne
        antenne = Antenne(mode='emetteur')
        
        with self.assertRaises(RuntimeError) as context:
            antenne.receive()
        
        self.assertIn("Cannot receive in emetteur mode", str(context.exception))

if __name__ == '__main__':
    unittest.main()

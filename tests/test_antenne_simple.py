"""
Tests unitaires simplifiés pour le module Antenne
"""
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# IMPORTANT: Importer les mocks MicroPython AVANT tout autre import
from tests.micropython_mocks import setup_micropython_mocks
setup_micropython_mocks()

import unittest
from source.antenne import Antenne

class TestAntenne(unittest.TestCase):
    
    def test_init_emetteur_mode(self):
        """Test l'initialisation en mode émetteur"""
        antenne = Antenne(mode='emetteur')
        
        self.assertEqual(antenne.mode, 'emetteur')
        self.assertEqual(antenne._address, b"2Node")
        self.assertEqual(antenne._channel, 76)
        self.assertEqual(antenne._payload_size, 32)
    
    def test_init_recepteur_mode(self):
        """Test l'initialisation en mode récepteur"""
        antenne = Antenne(mode='recepteur')
        self.assertEqual(antenne.mode, 'recepteur')
    
    def test_init_invalid_mode(self):
        """Test l'initialisation avec un mode invalide"""
        with self.assertRaises(ValueError) as context:
            Antenne(mode='invalid')
        
        self.assertIn("mode must be 'emetteur' or 'recepteur'", str(context.exception))
    
    def test_send_string_success(self):
        """Test l'envoi d'un message string avec succès"""
        antenne = Antenne(mode='emetteur')
        result = antenne.send("Hello World")
        self.assertTrue(result)
    
    def test_send_bytes_success(self):
        """Test l'envoi d'un message bytes avec succès"""
        antenne = Antenne(mode='emetteur')
        result = antenne.send(b"Hello Bytes")
        self.assertTrue(result)
    
    def test_send_dict_success(self):
        """Test l'envoi d'un dictionnaire avec succès"""
        antenne = Antenne(mode='emetteur')
        test_dict = {"test": "value"}
        result = antenne.send(test_dict)
        self.assertTrue(result)
    
    def test_send_in_recepteur_mode(self):
        """Test l'envoi en mode récepteur (doit lever une exception)"""
        antenne = Antenne(mode='recepteur')
        
        with self.assertRaises(RuntimeError) as context:
            antenne.send("Hello")
        
        self.assertIn("Cannot send in recepteur mode", str(context.exception))
    
    def test_receive_string_message(self):
        """Test la réception d'un message string"""
        antenne = Antenne(mode='recepteur')
        
        # Ajouter un message au mock
        antenne.nrf.add_message(b"Hello World")
        
        result = antenne.receive()
        self.assertEqual(result, "Hello World")
    
    def test_receive_json_message(self):
        """Test la réception d'un message JSON"""
        antenne = Antenne(mode='recepteur')
        
        # Ajouter un message JSON au mock (commence par 'J')
        antenne.nrf.add_message(b'J{"test": "value"}')
        
        result = antenne.receive()
        self.assertEqual(result, {"test": "value"})
    
    def test_receive_no_message(self):
        """Test la réception quand il n'y a pas de message"""
        antenne = Antenne(mode='recepteur')
        result = antenne.receive()
        self.assertIsNone(result)
    
    def test_receive_in_emetteur_mode(self):
        """Test la réception en mode émetteur (doit lever une exception)"""
        antenne = Antenne(mode='emetteur')
        
        with self.assertRaises(RuntimeError) as context:
            antenne.receive()
        
        self.assertIn("Cannot receive in emetteur mode", str(context.exception))

if __name__ == '__main__':
    unittest.main()

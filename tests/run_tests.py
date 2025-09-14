"""
Script pour exécuter tous les tests unitaires
"""
import sys
import os

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# IMPORTANT: Importer les mocks MicroPython AVANT tout autre import
from tests.micropython_mocks import setup_micropython_mocks
setup_micropython_mocks()

import unittest

def run_all_tests():
    """Exécute tous les tests unitaires"""
    # Découvrir et charger tous les tests
    loader = unittest.TestLoader()
    test_dir = os.path.dirname(__file__)
    suite = loader.discover(test_dir, pattern='test_*.py')
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Retourner le code de sortie approprié
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_all_tests())

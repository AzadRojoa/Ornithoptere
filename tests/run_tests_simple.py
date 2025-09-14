"""
Script pour exécuter tous les tests unitaires simplifiés
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
    """Exécute tous les tests unitaires simplifiés"""
    print("🧪 Exécution des tests unitaires pour Ornithoptere\n")
    
    # Liste des modules de test à exécuter
    test_modules = [
        'tests.test_bouton',
        'tests.test_logger', 
        'tests.test_joystick_simple',
        'tests.test_moteur_simple',
        'tests.test_servomoteurs_simple',
        'tests.test_antenne_simple'
    ]
    
    # Découvrir et charger tous les tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for module_name in test_modules:
        try:
            tests = loader.loadTestsFromName(module_name)
            suite.addTests(tests)
        except Exception as e:
            print(f"❌ Erreur lors du chargement de {module_name}: {e}")
    
    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Afficher le résumé
    print(f"\n📊 Résultats des tests:")
    print(f"   ✅ Tests réussis: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   ❌ Tests échoués: {len(result.failures)}")
    print(f"   💥 Erreurs: {len(result.errors)}")
    print(f"   📈 Total: {result.testsRun}")
    
    if result.wasSuccessful():
        print("\n🎉 Tous les tests ont réussi!")
    else:
        print("\n⚠️  Certains tests ont échoué.")
    
    # Retourner le code de sortie approprié
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_all_tests())

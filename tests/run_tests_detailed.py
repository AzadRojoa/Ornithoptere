"""
Script pour exécuter les tests avec maximum de détails
"""
import sys
import os
import unittest

# Ajouter le répertoire racine au path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# IMPORTANT: Importer les mocks MicroPython AVANT tout autre import
from tests.micropython_mocks import setup_micropython_mocks
setup_micropython_mocks()

def run_detailed_tests():
    """Exécute les tests avec le maximum de détails"""
    print("🔍 Exécution des tests avec détails complets\n")
    
    # Liste des modules de test à exécuter
    test_modules = [
        'tests.test_bouton',
        'tests.test_logger', 
        'tests.test_joystick',
        'tests.test_moteur',
        'tests.test_servomoteurs',
        'tests.test_antenne'
    ]
    
    # Découvrir et charger tous les tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    for module_name in test_modules:
        try:
            tests = loader.loadTestsFromName(module_name)
            suite.addTests(tests)
            print(f"✅ Module {module_name} chargé")
        except Exception as e:
            print(f"❌ Erreur lors du chargement de {module_name}: {e}")
    
    print(f"\n📊 {suite.countTestCases()} tests trouvés\n")
    
    # Classe personnalisée pour afficher plus de détails
    class DetailedTestResult(unittest.TextTestResult):
        def startTest(self, test):
            super().startTest(test)
            print(f"🔄 DÉBUT: {test._testMethodName} ({test.__class__.__name__})")
        
        def addSuccess(self, test):
            super().addSuccess(test)
            print(f"✅ RÉUSSI: {test._testMethodName}")
        
        def addError(self, test, err):
            super().addError(test, err)
            print(f"💥 ERREUR: {test._testMethodName}")
            print(f"   {err[1]}")
        
        def addFailure(self, test, err):
            super().addFailure(test, err)
            print(f"❌ ÉCHEC: {test._testMethodName}")
            print(f"   {err[1]}")
    
    # Runner personnalisé
    class DetailedTestRunner(unittest.TextTestRunner):
        resultclass = DetailedTestResult
    
    # Exécuter les tests
    runner = DetailedTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)
    
    # Résumé final
    print(f"\n🎯 RÉSUMÉ FINAL:")
    print(f"   📈 Total de tests: {result.testsRun}")
    print(f"   ✅ Réussis: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"   ❌ Échecs: {len(result.failures)}")
    print(f"   💥 Erreurs: {len(result.errors)}")
    
    if result.failures:
        print(f"\n🔍 DÉTAILS DES ÉCHECS:")
        for test, traceback in result.failures:
            print(f"   ❌ {test}: {traceback}")
    
    if result.errors:
        print(f"\n🔍 DÉTAILS DES ERREURS:")
        for test, traceback in result.errors:
            print(f"   💥 {test}: {traceback}")
    
    if result.wasSuccessful():
        print("\n🎉 TOUS LES TESTS ONT RÉUSSI! 🎉")
    else:
        print("\n⚠️ CERTAINS TESTS ONT ÉCHOUÉ!")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_detailed_tests())

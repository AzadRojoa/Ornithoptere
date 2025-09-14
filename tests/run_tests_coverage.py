"""
Script pour exécuter les tests avec coverage
"""
import os
import sys
import subprocess

def run_tests_with_coverage():
    """Exécute les tests avec mesure de la couverture de code"""
    print("🧪 Exécution des tests unitaires avec couverture de code...\n")
    
    # Répertoire du projet
    project_dir = os.path.dirname(os.path.dirname(__file__))
    source_dir = os.path.join(project_dir, 'source')
    tests_dir = os.path.join(project_dir, 'tests')
    
    try:
        # Installer les dépendances de test si coverage n'est pas disponible
        try:
            import coverage
        except ImportError:
            print("📦 Installation de coverage...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'coverage'], check=True)
        
        # Commandes pour exécuter les tests avec coverage
        commands = [
            # Démarrer la mesure de coverage
            ['coverage', 'erase'],
            
            # Exécuter les tests avec coverage
            ['coverage', 'run', '--source', source_dir, '-m', 'unittest', 'discover', '-s', tests_dir, '-p', 'test_*.py', '-v'],
            
            # Générer le rapport
            ['coverage', 'report', '-m'],
            
            # Générer le rapport HTML
            ['coverage', 'html', '--directory', os.path.join(project_dir, 'htmlcov')]
        ]
        
        for cmd in commands:
            print(f"🔄 Exécution: {' '.join(cmd)}")
            result = subprocess.run(cmd, cwd=project_dir)
            if result.returncode != 0 and cmd[1] != 'erase':  # erase peut échouer si pas de fichier .coverage
                print(f"❌ Erreur lors de l'exécution de: {' '.join(cmd)}")
                return result.returncode
            print()
        
        print("✅ Tests terminés avec succès!")
        print(f"📊 Rapport HTML généré dans: {os.path.join(project_dir, 'htmlcov', 'index.html')}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(run_tests_with_coverage())

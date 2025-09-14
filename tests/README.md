# Tests Unitaires pour Ornithoptere

Ce répertoire contient tous les tests unitaires pour les modules du projet Ornithoptere.

## 📁 Structure

```
tests/
├── __init__.py
├── micropython_mocks.py          # Système de mocks pour MicroPython  
├── README.md                     # Cette documentation
├── run_tests.py                  # Runner principal
├── run_tests_detailed.py         # Runner avec affichage détaillé
├── run_tests_coverage.py         # Runner avec mesure de couverture
├── test_antenne.py              # Tests du module antenne
├── test_bouton.py               # Tests du module bouton
├── test_joystick.py             # Tests du module joystick  
├── test_logger.py               # Tests du module logger
├── test_moteur.py               # Tests du module moteur
└── test_servomoteurs.py         # Tests du module servomoteurs
```

## 🚀 Exécution des tests

### ⭐ Méthode recommandée - Tous les tests
```bash
python3 tests/run_tests.py
```

### 🔍 Voir chaque test en détail
```bash
python3 tests/run_tests_detailed.py
```

### 📊 Avec mesure de couverture
```bash
python3 tests/run_tests_coverage.py
```

### 🎯 Tests par module
```bash
python3 tests/test_bouton.py
python3 tests/test_logger.py
python3 tests/test_joystick.py
python3 tests/test_moteur.py
python3 tests/test_servomoteurs.py
python3 tests/test_antenne.py
```

### 📝 Avec unittest verbose
```bash
python3 -m unittest tests.test_bouton -v
python3 -m unittest tests.test_logger -v
python3 -m unittest tests.test_joystick -v
python3 -m unittest tests.test_moteur -v
python3 -m unittest tests.test_servomoteurs -v
python3 -m unittest tests.test_antenne -v
```
```bash
python3 tests/run_tests_coverage.py
```

## Système de Mocks

Le fichier `micropython_mocks.py` contient un système complet de simulation des modules MicroPython :

### Modules mockés
- `machine.Pin` : Contrôle des GPIO
- `machine.ADC` : Convertisseurs analogique-numérique
- `machine.PWM` : Modulation de largeur d'impulsion
- `machine.SPI` : Communication SPI
- `nrf24l01.NRF24L01` : Module de communication radio
- `ujson` : Sérialization JSON pour MicroPython
- `time` : Fonctions de temps
- `logging` : Système de logs

### Avantages du système de mocks
- ✅ Pas besoin de hardware réel
- ✅ Tests reproductibles et rapides
- ✅ Simulation du comportement hardware
- ✅ Gestion des erreurs et cas limites
- ✅ Compatible avec Python standard

## Couverture des tests

### Résultats actuels
```
📊 Résultats des tests:
   ✅ Tests réussis: 52
   ❌ Tests échoués: 0
   💥 Erreurs: 0
   📈 Total: 52
```

### Modules testés

#### 🔘 Bouton (7 tests)
- Initialisation avec différents paramètres
- Lecture de l'état du bouton (`is_pressed()`)
- Propriétés `value` et `pin`
- Méthode `__str__()`

#### 🕹️ Joystick (6 tests)
- Initialisation avec différentes configurations
- Lecture des valeurs analogiques X et Y
- Lecture de l'état du bouton
- Méthode `read()` qui retourne un tuple
- Méthode `__str__()`

#### 📝 Logger (9 tests)
- Initialisation avec différents noms de fichiers
- Méthodes de logging (debug, info, warning, error)
- Formatage des timestamps
- Gestion des erreurs de fichier

#### ⚙️ Moteur (9 tests)
- Initialisation avec différentes fréquences
- Méthode `set_speed()`
- Propriétés `duty`, `frequency`, et `speed`
- Conversions entre pourcentage et duty cycle

#### 🔄 ServoMoteur (10 tests)
- Initialisation avec différents paramètres
- Méthode `angle()` avec différents degrés (0°, 90°, 180°)
- Propriétés `frequency` et `deg`
- Calculs de duty cycle basés sur les microsecondes
- Plages personnalisées de microsecondes

#### 📡 Antenne (11 tests)
- Initialisation en mode émetteur et récepteur
- Envoi de messages (string, bytes, dict)
- Réception de messages (string et JSON)
- Gestion des erreurs de communication
- Validation des modes de fonctionnement
- Sérialisation/désérialisation JSON

## Prérequis

- Python 3.6+
- Module `unittest` (inclus dans Python)
- Optionnel : `coverage` pour la mesure de couverture

```bash
# Installation des dépendances optionnelles
pip3 install -r tests/requirements-test.txt
```

## Notes techniques

### Pourquoi des tests simplifiés ?
Les tests `*_simple.py` utilisent le nouveau système de mocks qui simule automatiquement les modules MicroPython au lieu d'utiliser des mocks complexes avec `patch`. Cela rend les tests :
- Plus simples à écrire et maintenir
- Plus rapides à exécuter
- Plus fiables (moins de risques d'erreurs de mocking)

### Gestion des imports MicroPython
Le système de mocks doit être importé **AVANT** tous les autres modules pour intercepter correctement les imports MicroPython. C'est pourquoi chaque fichier de test commence par :

```python
from tests.micropython_mocks import setup_micropython_mocks
setup_micropython_mocks()
```

### Tests sur PC vs Hardware réel
Ces tests sont conçus pour valider la logique métier sur PC de développement. Pour des tests sur hardware réel, utilisez les modules directement sur un microcontrôleur compatible MicroPython.

## Contribution

Pour ajouter de nouveaux tests :

1. Créer un fichier `test_nouveaumodule_simple.py`
2. Importer le système de mocks en premier
3. Écrire les tests unitaires
4. Ajouter le module à la liste dans `run_tests_simple.py`

Exemple de structure :
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tests.micropython_mocks import setup_micropython_mocks
setup_micropython_mocks()

import unittest
from source.nouveaumodule import NouveauModule

class TestNouveauModule(unittest.TestCase):
    def test_something(self):
        # Votre test ici
        pass

if __name__ == '__main__':
    unittest.main()
```

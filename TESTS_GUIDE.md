# Tests Unitaires Ornithoptere - Guide de Démarrage Rapide

## 🚀 Démarrage Rapide

### Installation
```bash
# Aucune installation supplémentaire requise
# Les tests utilisent uniquement Python 3 et unittest (inclus)
```

### Exécution des Tests

#### ⭐ Méthode principale (recommandée)
```bash
# Exécuter tous les tests
./test.sh

# ou directement
python3 tests/run_tests_simple.py
```

#### 🎯 Tests par module
```bash
./test.sh test-module bouton       # Module Bouton
./test.sh test-module logger       # Module Logger  
./test.sh test-module joystick     # Module Joystick
./test.sh test-module moteur       # Module Moteur
./test.sh test-module servomoteurs # Module ServoMoteur
./test.sh test-module antenne      # Module Antenne
```

#### 📊 Tests avec couverture
```bash
./test.sh coverage
```

## 📋 Résultats Attendus

```
🧪 Exécution des tests unitaires pour Ornithoptere

[52 tests détaillés...]

----------------------------------------------------------------------
Ran 52 tests in 0.017s

OK

📊 Résultats des tests:
   ✅ Tests réussis: 52
   ❌ Tests échoués: 0
   💥 Erreurs: 0
   📈 Total: 52

🎉 Tous les tests ont réussi!
```

## 📁 Structure des Tests

```
tests/
├── micropython_mocks.py       # ⚙️ Système de simulation MicroPython
├── run_tests_simple.py        # 🎯 Script principal
├── test_bouton.py             # 🔘 Tests Bouton (7 tests)
├── test_logger.py             # 📝 Tests Logger (9 tests)  
├── test_joystick_simple.py    # 🕹️ Tests Joystick (6 tests)
├── test_moteur_simple.py      # ⚙️ Tests Moteur (9 tests)
├── test_servomoteurs_simple.py # 🔄 Tests ServoMoteur (10 tests)
└── test_antenne_simple.py     # 📡 Tests Antenne (11 tests)
```

## 🛠️ Fonctionnalités Testées

| Module | Tests | Couverture |
|--------|-------|------------|
| **Bouton** | 7 | ✅ Initialisation, lecture état, propriétés |
| **Logger** | 9 | ✅ Logs, timestamps, gestion erreurs |
| **Joystick** | 6 | ✅ Axes X/Y, bouton, lecture complète |
| **Moteur** | 9 | ✅ Vitesse, PWM, duty cycle |
| **ServoMoteur** | 10 | ✅ Angles, positions, calculs µs |
| **Antenne** | 11 | ✅ RF émission/réception, JSON |

## 🔧 Commandes Utiles

```bash
# Aide
./test.sh help

# Nettoyage
./test.sh clean

# Installation dépendances (optionnel)
./test.sh install-deps

# Test individuel
python3 tests/test_bouton.py

# Unittest verbose
python3 -m unittest tests.test_bouton -v
```

## 🎯 Intégration VS Code

Les tests sont automatiquement détectés dans VS Code :
- **Ctrl+Shift+P** → "Python: Run All Tests"
- Panel Test Explorer disponible
- Tasks configurées (Ctrl+Shift+P → "Tasks: Run Task")

## ✨ Avantages

- ✅ **52 tests** couvrant tous les modules
- ✅ **Simulation hardware** complète
- ✅ **Exécution rapide** (< 1 seconde)
- ✅ **Pas de dépendances** hardware
- ✅ **Compatible CI/CD** (GitHub Actions inclus)
- ✅ **Documentation** complète

## 🎉 Vous êtes prêt !

Vos modules sont maintenant **entièrement testés** avec une suite complète de tests unitaires. 

Exécutez `./test.sh` pour voir tous vos tests passer ! 🚀

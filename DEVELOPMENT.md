# Guide de développement - Pre-commit

## Installation

Pour installer pre-commit et configurer les hooks, exécutez :

```bash
./setup-precommit.sh
```

Ou manuellement :

```bash
# Installer les dépendances
pip install -r requirements-dev.txt

# Installer les hooks pre-commit
pre-commit install

# Tester les hooks sur tous les fichiers
pre-commit run --all-files
```

## Hooks configurés

Les hooks suivants s'exécutent automatiquement avant chaque commit :

### 1. Formatage et style
- **Black** : Formatage automatique du code Python
- **isort** : Tri automatique des imports
- **flake8** : Vérification du style et des erreurs potentielles

### 2. Tests
- **pytest** : Exécution des tests unitaires dans `source/tests/`

### 3. Vérifications générales
- Suppression des espaces en fin de ligne
- Ajout d'une ligne vide en fin de fichier
- Vérification de la syntaxe YAML
- Détection des gros fichiers
- Détection des conflits de merge
- Détection des instructions de debug

## Commandes utiles

```bash
# Exécuter tous les hooks manuellement
pre-commit run --all-files

# Exécuter un hook spécifique
pre-commit run black
pre-commit run flake8
pre-commit run pytest

# Bypasser les hooks (non recommandé)
git commit --no-verify

# Mettre à jour les hooks
pre-commit autoupdate

# Désinstaller les hooks
pre-commit uninstall
```

## Configuration

Les fichiers de configuration sont :
- `.pre-commit-config.yaml` : Configuration des hooks
- `.flake8` : Configuration du linter
- `.isort.cfg` : Configuration du tri des imports
- `pyproject.toml` : Configuration Black et pytest

## Résolution des problèmes

Si un hook échoue :

1. **Black ou isort** : Les fichiers sont automatiquement formatés, ajoutez-les et recommitez
2. **flake8** : Corrigez les erreurs de style reportées
3. **pytest** : Corrigez les tests qui échouent
4. **Autres hooks** : Suivez les instructions d'erreur

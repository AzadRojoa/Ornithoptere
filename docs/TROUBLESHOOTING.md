# 🔧 Dépannage pre-commit

## Problèmes courants et solutions

### ❌ "Command not found: pre-commit"

**Cause :** L'environnement virtuel n'est pas activé.

**Solution :**
```bash
source .venv/bin/activate
```

### ❌ "Your pre-commit configuration is unstaged"

**Cause :** La configuration pre-commit a été modifiée mais pas ajoutée au commit.

**Solution :**
```bash
git add .pre-commit-config.yaml
git commit -m "Votre message"
```

### ❌ Tests qui échouent (pytest)

**Cause :** Votre code a cassé des tests existants.

**Solutions :**
1. **Voir les erreurs détaillées :**
   ```bash
   ./scripts/run-tests.sh
   ```

2. **Corriger les erreurs dans votre code**

3. **Vérifier que les tests passent :**
   ```bash
   pre-commit run pytest
   ```

### ❌ Erreurs flake8 (style de code)

**Exemples d'erreurs courantes :**
- `E501 line too long` → Raccourcir la ligne ou la diviser
- `F401 imported but unused` → Supprimer l'import inutile
- `E302 expected 2 blank lines` → Ajouter des lignes vides

**Solution :** Corriger manuellement ou utiliser un éditeur avec support flake8.

### ❌ "files were modified by this hook"

**Cause :** Black ou isort ont formaté automatiquement votre code.

**Solution :** C'est normal ! Ajoutez les changements :
```bash
git add .
git commit -m "Votre message"
```

### 🚨 En cas d'urgence absolue

**Si vous devez absolument commiter sans vérifications :**
```bash
git commit --no-verify -m "Votre message"
```

⚠️ **Attention :** À utiliser uniquement en cas d'urgence ! Cela contourne toutes les vérifications de qualité.

## Vérifications manuelles

```bash
# Vérifier tous les hooks
pre-commit run --all-files

# Vérifier un hook spécifique
pre-commit run black
pre-commit run flake8
pre-commit run pytest

# Mettre à jour les hooks
pre-commit autoupdate

# Désinstaller pre-commit (non recommandé)
pre-commit uninstall
```

## Configuration de votre éditeur

### VS Code
Installez les extensions :
- Python
- Black Formatter
- isort
- Flake8

### PyCharm
- Activez Black dans Settings → Tools → External Tools
- Configurez flake8 dans Settings → Editor → Inspections

---

💡 **Conseil :** Configurez votre éditeur pour formater automatiquement avec Black et afficher les erreurs flake8. Cela vous évitera la plupart des problèmes pre-commit !

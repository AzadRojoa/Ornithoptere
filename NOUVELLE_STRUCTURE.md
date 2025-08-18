# Nouvelle Structure Unifiée

## Vue d'ensemble

Le code a été refactorisé pour séparer clairement les aspects simulation et réel, tout en unifiant les programmes d'émission et réception.

## Structure des fichiers

### Fichiers principaux
- `programme_antenne_unifie.py` - Programme principal unifié avec arguments CLI
- `emetteur_esp32.py` - Fichier dédié pour ESP32 émetteur (pas d'arguments)
- `recepteur_esp32.py` - Fichier dédié pour ESP32 récepteur (pas d'arguments)
- `simulation_helper.py` - Module qui gère toutes les fonctionnalités spécifiques à la simulation
- `lancer_antenne.sh` - Script de lancement interactif

### Fichiers conservés
- `tableau_terminal.py` - Affichage en tableau (amélioré avec info_box)
- `keyboard_controller.py` - Contrôleur clavier (amélioré avec toggle)
- `components.py`, `gamepad.py`, `antenne.py` - Composants de base
- Dossiers `simulation_pc/` et `tests/` - Inchangés

### Fichiers de scripts
- `scripts/deploy.sh` - Déploiement automatique sur ESP32 avec mpfshell (mis à jour)
- `lancer_antenne.sh` - Script de lancement interactif pour tests PC

## Utilisation

### Méthode 1 : Script interactif (recommandé)
```bash
./lancer_antenne.sh
```
Puis choisir le mode voulu (1-6).

### Méthode 2 : Ligne de commande directe (PC)
```bash
# Émetteur réel ESP32 (par défaut)
python source/programme_antenne_unifie.py emetteur

# Récepteur réel ESP32 (par défaut)
python source/programme_antenne_unifie.py recepteur

# Émetteur simulation
python source/programme_antenne_unifie.py emetteur --simulation

# Récepteur simulation
python source/programme_antenne_unifie.py recepteur --simulation
```

### Méthode 3 : Déploiement automatique ESP32
```bash
# Déploiement automatique avec mpfshell
./scripts/deploy.sh
# Choisir émetteur ou récepteur, le script fait le reste !
```

### Méthode 4 : Déploiement manuel ESP32
```bash
# Copier manuellement les fichiers essentiels :
# - emetteur_esp32.py → main.py (ou recepteur_esp32.py)
# - programme_antenne_unifie.py
# - simulation_helper.py
# - tableau_terminal.py
# - components.py
# - gamepad.py (émetteur seulement)
# - antenne.py
```

## Avantages de cette structure

1. **Code plus propre** : Séparation claire simulation/réel
2. **Maintenance simplifiée** : Un seul fichier principal au lieu de deux
3. **Réutilisabilité** : Le module `simulation_helper` peut être réutilisé
4. **Flexibilité** : Arguments de ligne de commande + fichiers ESP32 dédiés
5. **DRY principle** : Plus de duplication de code entre émetteur/récepteur
6. **Déploiement ESP32 simplifié** : Fichiers dédiés sans arguments CLI

## Migration

Les anciens fichiers `programme_antenne_emission.py` et `programme_antenne_reception.py` peuvent être conservés pour compatibilité ou supprimés si vous utilisez la nouvelle structure.

## Fonctionnalités conservées

- ✅ Contrôles clavier avec toggle des boutons
- ✅ Affichage en tableau avec titre et info_box
- ✅ Support simulation et mode réel
- ✅ Gestion des deux joysticks J1 et J2
- ✅ États visuels avec emojis
- ✅ Arrêt propre avec Ctrl+C

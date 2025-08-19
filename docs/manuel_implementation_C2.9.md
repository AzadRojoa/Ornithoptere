# Manuel d'Implémentation - Système de Contrôle Ornithoptère
**Version 1.0 - Août 2025**

## Sommaire

1. [Introduction et objectifs](#1-introduction-et-objectifs)
2. [Architecture du système](#2-architecture-du-système)
3. [Modules développés](#3-modules-développés)
4. [Installation et démarrage](#4-installation-et-démarrage)
5. [Configuration et personnalisation](#5-configuration-et-personnalisation)
6. [Utilisation des modules](#6-utilisation-des-modules)
7. [Mises à jour](#7-mises-à-jour)
8. [Dépannage](#8-dépannage)

---

## 1. Introduction et objectifs

### 1.1 Objectif du manuel
Ce manuel explique comment utiliser et intégrer les modules développés pour le système de contrôle Ornithoptère. Il s'adresse aux développeurs et intégrateurs qui souhaitent comprendre et utiliser le système sans entrer dans les détails techniques complexes.

### 1.2 Public cible
- **Développeurs** : Comprendre l'architecture et les modules
- **Intégrateurs** : Déployer et configurer le système
- **Techniciens** : Maintenir et dépanner le système

### 1.3 Philosophie du projet
Le système a été conçu pour être :
- **Simple** : Installation et utilisation facilitées
- **Modulaire** : Chaque composant a un rôle spécifique
- **Flexible** : Adaptable à différents besoins
- **Robuste** : Gestion d'erreurs et récupération automatique

## 2. Architecture du système

### 2.1 Vue d'ensemble
Le système Ornithoptère est composé de deux parties principales qui communiquent par radio :

```
┌─────────────────┐    Radio 2.4GHz    ┌─────────────────┐
│   ÉMETTEUR      │ ◄─────────────────► │   RÉCEPTEUR     │
│                 │                     │                 │
│ • Joysticks     │                     │ • Moteurs       │
│ • Interface     │                     │ • Servos        │
│ • Transmission  │                     │ • Contrôle vol  │
└─────────────────┘                     └─────────────────┘
```

### 2.2 Environnements supportés
- **Développement** : Simulation complète sur PC Linux
- **Production** : ESP32 avec hardware réel
- **Test** : Mélange PC Linux + ESP32

### 2.3 Communication
- **Type** : Radio NRF24L01 (2.4GHz)
- **Portée** : 100m en extérieur, 30m en intérieur
- **Fréquence** : 10 commandes/seconde
- **Sécurité** : Arrêt automatique si perte de signal

## 3. Modules développés

### 3.1 Module `antenne.py` - Cœur de la communication
**Rôle** : Gère toute la communication radio entre émetteur et récepteur

**Ce qu'il fait** :
- Configure automatiquement la radio NRF24L01
- Encode/décode les messages de façon transparente
- Gère la connexion et les erreurs de transmission
- Assure la synchronisation entre les deux modules

**Comment l'utiliser** :
```python
# Créer une antenne émettrice
antenne = Antenne(mode="emetteur")
antenne.envoyer_donnees(donnees_joysticks)

# Créer une antenne réceptrice  
antenne = Antenne(mode="recepteur")
donnees = antenne.recevoir_donnees()
```

### 3.2 Module `components.py` - Gestion du hardware
**Rôle** : Interface entre le logiciel et les composants physiques

**Composants gérés** :
- **Joystick** : Lecture des positions X/Y et boutons
- **Moteur** : Contrôle de vitesse des moteurs brushless
- **ServoMoteur** : Positionnement précis des servos
- **LED** : Indicateurs visuels d'état

**Ce qu'il fait** :
- Simplifie la lecture des capteurs
- Convertit automatiquement les valeurs (0-100% au lieu de 0-1023)
- Gère les limitations de sécurité
- Lisse les variations pour éviter les à-coups

**Exemple d'utilisation** :
```python
# Lire un joystick
joystick = Joystick(pin_x=36, pin_y=39, pin_bouton=32)
position = joystick.lire()  # Retourne {x: 50, y: -30, bouton: False}

# Contrôler un moteur
moteur = Moteur(pin=5)
moteur.set_vitesse(75)  # 75% de la vitesse maximum
```

### 3.3 Module `gamepad.py` - Interface de contrôle
**Rôle** : Transforme les joysticks physiques en commandes de vol

**Ce qu'il fait** :
- Lit en continu les positions des joysticks
- Applique une zone morte pour éviter les micro-mouvements
- Convertit les positions en commandes compréhensibles
- Gère les boutons spéciaux (arrêt d'urgence, etc.)

**Fonctionnalités** :
- **Joystick 1** : Contrôle principal (vitesse, direction)
- **Joystick 2** : Contrôles auxiliaires (servos, fonctions spéciales)
- **Boutons** : Actions spéciales et sécurité

### 3.4 Module `flight_controler.py` - Contrôleur de vol
**Rôle** : Transforme les commandes reçues en actions sur les moteurs

**Ce qu'il fait** :
- Reçoit les commandes de l'émetteur
- Calcule la puissance nécessaire pour chaque moteur
- Applique les limites de sécurité
- Gère l'arrêt d'urgence automatique

**Sécurités intégrées** :
- Arrêt automatique si perte de signal (200ms)
- Limitation de puissance pour éviter la surchauffe
- Validation des commandes reçues
- Mode dégradé en cas de problème

### 3.5 Module `tableau_terminal.py` - Interface utilisateur
**Rôle** : Affiche les informations en temps réel

**Ce qu'il affiche** :
- État de la connexion radio
- Positions des joysticks en temps réel
- État des moteurs et servos
- Messages d'erreur et d'information
- Statistiques de performance

**Avantages** :
- Interface claire et colorée
- Mise à jour en temps réel (20 fois par seconde)
- Accessible depuis un terminal standard
- Idéal pour le debug et la supervision

### 3.6 Module `logger.py` - Enregistrement des données
**Rôle** : Enregistre tout ce qui se passe pour le debug et l'analyse

**Ce qu'il enregistre** :
- Toutes les commandes envoyées/reçues
- Erreurs et événements système
- Statistiques de performance
- État des composants hardware

**Formats disponibles** :
- Fichiers texte pour lecture humaine
- Fichiers CSV pour analyse dans Excel
- Logs système Linux standard

## 4. Installation et démarrage

### 4.1 Installation automatique
Le projet inclut un script d'installation qui fait tout automatiquement :

```bash
# Cloner le projet
git clone [URL_DU_PROJET] ornithoptere
cd ornithoptere

# Installation automatique
chmod +x install.sh
./install.sh
```

**Ce que fait le script** :
- Installe Python et les dépendances nécessaires
- Configure l'environnement de développement
- Teste que tout fonctionne correctement
- Crée les raccourcis pour le lancement

### 4.2 Premier démarrage - Mode simulation
Avant d'utiliser le hardware réel, testez en simulation :

```bash
# Lancer le script interactif
./start-simu.sh

# Choisir "Simulation émetteur + récepteur"
# Utiliser les touches du clavier pour simuler les joysticks
```

### 4.3 Déploiement sur ESP32
Une fois la simulation validée, déployez sur le hardware :

```bash
# Connecter vos ESP32 en USB
# Lancer le déploiement automatique
./deploy_esp32.sh

# Le script détecte automatiquement les ESP32
# Choisir émetteur ou récepteur pour chaque ESP32
```

## 5. Configuration et personnalisation

### 5.1 Configuration de base
Tous les paramètres importants sont dans `source/antenne.py` :

**Canal radio** : Si vous avez des interférences, changez le canal
```python
CHANNEL = 76  # Valeur par défaut, essayez 100 ou 120
```

**Puissance de transmission** : Ajustez selon la portée souhaitée
```python
POWER_LEVEL = 0x06  # Maximum pour longue portée
POWER_LEVEL = 0x02  # Minimum pour économiser la batterie
```

### 5.2 Personnalisation des contrôles
Dans `source/gamepad.py`, vous pouvez modifier :

**Zone morte des joysticks** : Évite les micro-mouvements
```python
DEAD_ZONE = 50  # Augmentez si les joysticks "driftent"
```

**Sensibilité** : Ajustez la réactivité
```python
SENSITIVITY = 1.0  # 0.5 = moins sensible, 2.0 = plus sensible
```

### 5.3 Configuration des moteurs
Dans `source/components.py` :

**Fréquence PWM** : Selon le type de moteurs
```python
MOTOR_FREQ = 1000  # Hz, pour moteurs brushed standard
MOTOR_FREQ = 8000  # Hz, pour moteurs brushless
```

**Limites de vitesse** : Pour la sécurité
```python
MAX_SPEED = 80  # Limite à 80% pour les tests
```

## 6. Utilisation des modules

### 6.1 Créer un émetteur personnalisé
```python
from source.antenne import Antenne
from source.gamepad import Gamepad

# Initialiser les composants
antenne = Antenne(mode="emetteur")
gamepad = Gamepad()

# Boucle principale
while True:
    # Lire les commandes
    commandes = gamepad.lire_commandes()
    
    # Envoyer par radio
    antenne.envoyer_donnees(commandes)
    
    # Attendre 100ms
    time.sleep(0.1)
```

### 6.2 Créer un récepteur personnalisé
```python
from source.antenne import Antenne
from source.flight_controler import FlightControler

# Initialiser les composants
antenne = Antenne(mode="recepteur")
controleur = FlightControler()

# Boucle principale
while True:
    # Recevoir les commandes
    commandes = antenne.recevoir_donnees()
    
    if commandes:
        # Appliquer aux moteurs
        controleur.appliquer_commandes(commandes)
    else:
        # Arrêt de sécurité si pas de signal
        controleur.arret_urgence()
```

### 6.3 Utilisation avec interface graphique
Le module `tableau_terminal.py` peut être intégré partout :

```python
from source.tableau_terminal import TableauTerminal

# Créer l'interface
tableau = TableauTerminal()

# Dans votre boucle principale
tableau.afficher_donnees({
    'joystick_1': {'x': 50, 'y': -20},
    'joystick_2': {'x': 0, 'y': 30},
    'connexion': True,
    'signal': 85
})
```

## 7. Mises à jour

### 7.1 Pourquoi mettre à jour ?
Les mises à jour apportent :
- **Corrections de bugs** découverts en utilisation
- **Nouvelles fonctionnalités** demandées par les utilisateurs
- **Améliorations de performance** et de stabilité
- **Mises à jour de sécurité** importantes

### 7.2 Comment savoir qu'une mise à jour est disponible ?
Deux méthodes :
1. **Notification automatique** : Configurez GitHub pour recevoir un email
2. **Vérification manuelle** : Consultez la page "Releases" du projet

### 7.3 Processus de mise à jour simplifié
Le projet inclut un script qui fait tout automatiquement :

```bash
# Lancer la mise à jour
./mise-a-jour.sh

# Le script :
# 1. Sauvegarde votre version actuelle
# 2. Télécharge la nouvelle version
# 3. Met à jour vos ESP32 automatiquement
# 4. Teste que tout fonctionne
# 5. Vous guide pour valider
```

### 7.4 Sécurité des mises à jour
**Sauvegarde automatique** : Votre version actuelle est toujours sauvegardée
```bash
# Si problème, restaurer l'ancienne version
./restaurer-version-precedente.sh
```

**Test automatique** : Le script vérifie que tout fonctionne avant de valider

**Étapes graduelles** : Vous pouvez arrêter à tout moment

### 7.5 Types de mises à jour
**Mises à jour mineures** (v1.2.1 → v1.2.2) :
- Corrections de bugs
- Mise à jour automatique recommandée

**Mises à jour majeures** (v1.2 → v1.3) :
- Nouvelles fonctionnalités importantes
- Lisez les notes de version avant

**Mises à jour critiques** :
- Corrections de sécurité
- À appliquer rapidement

### 7.6 Bonnes pratiques
1. **Toujours tester** en simulation avant d'utiliser le hardware
2. **Lire les notes de version** pour comprendre les changements
3. **Garder une sauvegarde** de votre configuration personnalisée
4. **Mettre à jour régulièrement** pour avoir les dernières améliorations

## 8. Dépannage

### 8.1 Problèmes de communication radio

**Symptôme** : Pas de connexion entre émetteur et récepteur
**Solutions** :
1. Vérifier que les deux modules utilisent le même canal radio
2. Rapprocher les modules (test à 1 mètre)
3. Vérifier l'alimentation des modules NRF24L01 (3.3V exact)
4. Redémarrer les deux modules dans l'ordre : récepteur puis émetteur

**Symptôme** : Connexion instable, coupures fréquentes
**Solutions** :
1. Changer de canal radio (éviter 1-11 utilisés par WiFi)
2. Réduire la puissance de transmission
3. Vérifier les connexions des antennes
4. Éloigner des sources WiFi

### 8.2 Problèmes de joysticks

**Symptôme** : Joystick qui "dérive" (bouge tout seul)
**Solutions** :
1. Augmenter la zone morte dans la configuration
2. Calibrer le centre du joystick
3. Vérifier les connexions électriques

**Symptôme** : Joystick ne répond pas
**Solutions** :
1. Vérifier les connexions sur les bonnes pins
2. Tester avec un multimètre (tension 0-3.3V)
3. Vérifier l'alimentation 3.3V du joystick

### 8.3 Problèmes de moteurs

**Symptôme** : Moteurs ne tournent pas
**Solutions** :
1. Vérifier l'alimentation moteurs (séparée de l'ESP32)
2. Contrôler les connexions PWM
3. Tester avec des valeurs de debug

**Symptôme** : Moteurs saccadés ou bruyants
**Solutions** :
1. Ajuster la fréquence PWM selon le type de moteur
2. Vérifier la stabilité de l'alimentation
3. Ajouter un condensateur de filtrage si nécessaire

### 8.4 Problèmes logiciels

**Symptôme** : Le programme plante au démarrage
**Solutions** :
1. Vérifier les logs dans le terminal
2. Tester en mode simulation d'abord
3. Réinstaller avec le script automatique

**Symptôme** : Performance dégradée
**Solutions** :
1. Redémarrer les ESP32
2. Vérifier la mémoire disponible
3. Réduire la fréquence d'envoi si nécessaire

### 8.5 Où trouver de l'aide

1. **Logs système** : Consultez les fichiers dans `logs/`
2. **Mode debug** : Lancez avec l'option verbose pour plus d'informations
3. **Simulation** : Testez d'abord en simulation pour isoler les problèmes hardware
4. **Documentation** : Consultez le manuel d'exploitation pour les procédures de base

---

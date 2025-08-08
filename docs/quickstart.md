# 🚀 Guide d'utilisation

Ce guide explique comment utiliser le projet Ornithoptère, que vous soyez débutant ou que vous souhaitiez juste tester rapidement.

## 🎯 Deux façons d'utiliser le projet

### 1. 🧪 Mode Simulation (Recommandé pour débuter)
- Testez sans matériel ESP32
- Contrôlez avec votre clavier
- Idéal pour le développement

### 2. 🚁 Mode Réel (ESP32)
- Déployez sur de vrais ESP32
- Utilisez de vrais joysticks et servos
- Contrôle radio avec NRF24L01

---

## 🧪 Mode Simulation

### Étape 1 : Préparer l'environnement

```bash
cd Ornithoptere

# Installer les dépendances Python
pip install -r requirements.txt

# Vérifier que socat est installé (pour les ports virtuels)
sudo apt install socat  # Ubuntu/Debian
# ou
brew install socat     # macOS
```

### Étape 2 : Créer les ports série virtuels

```bash
# Lancer le script (laissez-le tourner)
./simulation_pc/creer_ports_serie.sh
```

Vous verrez :
```
🔧 Ports créés ! Vos programmes peuvent maintenant communiquer.
   Appuyez sur Ctrl+C pour arrêter les ports virtuels
```

### Étape 3 : Activer la simulation

Éditez `source/programme_antenne_emission.py` :

```python
SIMULATION = True  # Changez False en True
```

### Étape 4 : Lancer l'émetteur

```bash
# Dans un nouveau terminal
python3 source/programme_antenne_emission.py
```

### Étape 5 : Contrôler avec le clavier

Une fois lancé, vous pouvez contrôler les joysticks :

**Joystick J1 (gauche) :**
- `W/A/S/D` : Déplacer les axes
- `Espace` : Appuyer sur le bouton
- `R` : Centrer le joystick

**Joystick J2 (droite) :**
- `↑/←/↓/→` : Déplacer les axes
- `Entrée` : Appuyer sur le bouton
- `C` : Centrer le joystick

**Général :**
- `Z` : Centrer tous les joysticks
- `Ctrl+C` : Quitter

### Étape 6 : Lancer le récepteur (optionnel)

```bash
# Dans un troisième terminal
# Éditez d'abord source/programme_antenne_reception.py : SIMULATION = True
python3 source/programme_antenne_reception.py
```

---

## 🚁 Mode Réel (ESP32)

### Prérequis matériels

**Émetteur :**
- 1x ESP32
- 2x Joysticks analogiques
- 1x Module NRF24L01
- Alimentation/batterie

**Récepteur :**
- 1x ESP32
- 1x Module NRF24L01
- Servomoteurs/moteurs selon votre projet
- Alimentation/batterie

### Étape 1 : Préparer les ESP32

-  **Câbler les composants** selon le pinout

Voir [setup.md](setup.md) pour les détails techniques.

### Étape 2 : Déployer le code

#### Option A - Script automatique
```bash
./scripts/deploy.sh
```

#### Option B - Copie manuelle
Copiez ces fichiers vers vos ESP32 :

**Émetteur :**
```
source/programme_antenne_emission.py (SIMULATION = False)
source/components.py
source/gamepad.py
source/antenne.py
source/nrf24l01.py
source/tableau_terminal.py
```

**Récepteur :**
```
source/programme_antenne_reception.py (SIMULATION = False)
source/components.py
source/antenne.py
source/nrf24l01.py
source/flight_controler.py
```

### Étape 3 : Lancer les programmes

1. **Récepteur d'abord** : Démarrez l'ESP32 récepteur
2. **Puis l'émetteur** : Démarrez l'ESP32 émetteur
3. **Testez la connexion** : Bougez les joysticks

---

## 🔧 Conseils de développement

### Workflow recommandé

1. **Développez en simulation** - Testez votre logique
2. **Validez sur ESP32** - Déployez quand c'est stable
3. **Debuggez avec les logs** - Utilisez les messages de debug

### Modification du code

```python
# Pour basculer entre simulation et réel
SIMULATION = True   # Mode simulation
SIMULATION = False  # Mode ESP32
```

### Personnalisation

- **Joysticks** : Modifiez les pins dans `inputs = {...}`
- **Servos** : Ajustez dans le code récepteur
- **Fréquence radio** : Changez dans `antenne.py`

---

## ❓ Problèmes courants

### Simulation ne fonctionne pas
```bash
# Vérifiez que socat est installé
which socat

# Relancez les ports série
./simulation_pc/creer_ports_serie.sh
```

### ESP32 ne répond pas
- Vérifiez le câblage
- Testez la connexion série
- Consultez [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Contrôle clavier ne marche pas
- Assurez-vous d'être dans le bon terminal
- Le programme doit être en premier plan
- Testez avec des touches simples d'abord

---

**🎉 C'est tout ! Vous êtes prêt à piloter votre ornithoptère !**

Pour aller plus loin, consultez la [configuration avancée](setup.md) et l'[architecture](architecture.md).

# Simulation PC - Support série pour ESP32

Ce dossier contient les fichiers nécessaires pour faire fonctionner vos programmes ESP32 en mode simulation sur PC.

## 🎯 Principe

Vos programmes `programme_antenne_emission.py` et `programme_antenne_reception.py` peuvent maintenant fonctionner en **deux modes** :

- **Mode ESP32 réel** : `SIMULATION = False` (par défaut)
- **Mode simulation PC** : `SIMULATION = True`

## 📁 Fichiers dans ce dossier

| Fichier | Description |
|---------|-------------|
| `antenne_serial.py` | Classe de communication série (remplace NRF24L01 en simulation) |
| `creer_ports_serie.sh` | Script pour créer les ports série virtuels |
| `README.md` | Cette documentation |

## 🚀 Utilisation

### 1. Créer les ports série virtuels

```bash
cd simulation_pc
chmod +x creer_ports_serie.sh
./creer_ports_serie.sh
```

Laissez ce terminal ouvert (les ports restent actifs).

### 2. Activer le mode simulation

Dans vos programmes, changez :
```python
# En haut de programme_antenne_emission.py et programme_antenne_reception.py
SIMULATION = True  # Au lieu de False
```

### 3. Lancer vos programmes

**Terminal 2 - Récepteur :**
```bash
python3 source/programme_antenne_reception.py
```

**Terminal 3 - Émetteur :**
```bash
python3 source/programme_antenne_emission.py
```

## 📊 Données échangées

Format JSON des messages en simulation :
```json
{
  "J1": [2048, 2048, 0],  // [x, y, button] joystick 1
  "J2": [2048, 2048, 0]   // [x, y, button] joystick 2
}
```

## 🔧 Configuration

Ports série utilisés (modifiables dans vos programmes) :
- Émetteur : `/tmp/esp32_emetteur`
- Récepteur : `/tmp/esp32_recepteur`

## ✅ Avantages

✅ **Même code source** : Un seul programme pour les deux modes
✅ **Test facile** : Pas besoin d'ESP32 pour développer
✅ **Débug simple** : Messages visibles dans les terminaux
✅ **Transition fluide** : Changez juste `SIMULATION = True/False`

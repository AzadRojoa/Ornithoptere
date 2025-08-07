#!/bin/bash
#!/bin/bash
# Script simple pour créer les ports série virtuels pour la simulation

echo "🚀 PORTS SÉRIE VIRTUELS POUR SIMULATION ESP32"
echo "=============================================="
echo ""
echo "Ce script crée les ports série virtuels nécessaires"
echo "pour utiliser vos programmes avec SIMULATION = True"
echo ""
echo "📋 Usage :"
echo "  1. Lancez ce script (laissez-le tourner)"
echo "  2. Dans vos programmes .py, changez SIMULATION = True"
echo "  3. Lancez vos programmes dans des terminaux séparés :"
echo "     python3 source/programme_antenne_emission.py"
echo "     python3 source/programme_antenne_reception.py"
echo ""

# Vérification des dépendances
if ! command -v socat &> /dev/null; then
    echo "❌ socat manquant. Installation: sudo apt install socat"
    exit 1
fi

echo "✅ Dépendances OK"
echo ""
echo "📡 Création des ports série virtuels..."
echo "   /tmp/esp32_emetteur  <-> /tmp/esp32_recepteur"
echo ""
echo "🔧 Ports créés ! Vos programmes peuvent maintenant communiquer."
echo "   Appuyez sur Ctrl+C pour arrêter les ports virtuels"
echo ""

# Création et maintien des ports virtuels
socat -d -d pty,raw,echo=0,link=/tmp/esp32_emetteur pty,raw,echo=0,link=/tmp/esp32_recepteur

#!/bin/bash

echo "🚁 Système d'antenne Ornithoptère"
echo "=================================="
echo ""
echo "Choisissez le mode :"
echo "1) Émetteur (réel ESP32)"
echo "2) Récepteur (réel ESP32)"
echo "3) Émetteur (simulation PC)"
echo "4) Récepteur (simulation PC)"
echo "5) Test émetteur ESP32 (fichier dédié)"
echo "6) Test récepteur ESP32 (fichier dédié)"
echo ""

read -p "Votre choix (1-6): " choice

case $choice in
    1)
        echo "Lancement de l'émetteur en mode réel..."
        cd source && python programme_antenne_unifie.py emetteur
        ;;
    2)
        echo "Lancement du récepteur en mode réel..."
        cd source && python programme_antenne_unifie.py recepteur
        ;;
    3)
        echo "Lancement de l'émetteur en simulation..."
        cd source && python programme_antenne_unifie.py emetteur --simulation
        ;;
    4)
        echo "Lancement du récepteur en simulation..."
        cd source && python programme_antenne_unifie.py recepteur --simulation
        ;;
    5)
        echo "Test du fichier émetteur ESP32..."
        cd source && python emetteur_esp32.py
        ;;
    6)
        echo "Test du fichier récepteur ESP32..."
        cd source && python recepteur_esp32.py
        ;;
    *)
        echo "Choix invalide !"
        exit 1
        ;;
esac

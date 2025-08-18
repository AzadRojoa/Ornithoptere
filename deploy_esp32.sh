#!/bin/bash

echo "📡 Déploiement ESP32 - Ornithoptère"
echo "====================================="
echo ""
echo "Quel type d'ESP32 voulez-vous préparer ?"
echo "1) Émetteur ESP32"
echo "2) Récepteur ESP32"
echo ""

read -p "Votre choix (1-2): " choice

case $choice in
    1)
        echo "Préparation de l'émetteur ESP32..."
        echo ""
        echo "Fichiers à copier sur l'ESP32 émetteur :"
        echo "- source/emetteur_esp32.py → main.py"
        echo "- source/programme_antenne_unifie.py"
        echo "- source/simulation_helper.py"
        echo "- source/tableau_terminal.py"
        echo "- source/components.py"
        echo "- source/gamepad.py"
        echo "- source/antenne.py"
        echo ""
        echo "Puis renommer emetteur_esp32.py en main.py sur l'ESP32"
        ;;
    2)
        echo "Préparation du récepteur ESP32..."
        echo ""
        echo "Fichiers à copier sur l'ESP32 récepteur :"
        echo "- source/recepteur_esp32.py → main.py"
        echo "- source/programme_antenne_unifie.py"
        echo "- source/simulation_helper.py"
        echo "- source/tableau_terminal.py"
        echo "- source/antenne.py"
        echo ""
        echo "Puis renommer recepteur_esp32.py en main.py sur l'ESP32"
        ;;
    *)
        echo "Choix invalide !"
        exit 1
        ;;
esac

echo ""
echo "Note: Les fichiers de simulation (keyboard_controller, mock_machine, etc.)"
echo "ne sont pas nécessaires sur l'ESP32."

"""
Configuration pour l'émetteur ESP32
"""
# Importer le programme principal
import programme_antenne_unifie

# Configuration spécifique pour l'émetteur
ESP32_MODE = "emetteur"
SIMULATION = False

if __name__ == "__main__":
    programme_antenne_unifie.main()

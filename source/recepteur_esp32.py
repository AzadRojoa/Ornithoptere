"""
Configuration pour le récepteur ESP32
"""
# Importer le programme principal
import programme_antenne_unifie

# Configuration spécifique pour le récepteur
ESP32_MODE = "recepteur"
SIMULATION = False

if __name__ == "__main__":
    programme_antenne_unifie.main()

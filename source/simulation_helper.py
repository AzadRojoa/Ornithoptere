"""
Module d'aide pour la simulation - regroupe toutes les fonctionnalités spécifiques à la simulation
"""
import os
import sys
from typing import Dict, Optional


class SimulationHelper:
    """Classe qui gère tous les aspects spécifiques à la simulation"""

    def __init__(self, mode: str, port: str):
        self.mode = mode  # "emetteur" ou "recepteur"
        self.port = port
        self.keyboard_controller = None
        self.antenne = None

        # Configurer les imports mock
        self._setup_mock_imports()

        # Import de l'antenne série pour simulation
        sys.path.insert(
            0, os.path.join(os.path.dirname(__file__), "..", "simulation_pc")
        )
        from antenne_serial import AntenneSerial

        self.antenne = AntenneSerial(mode=mode, port=port)

    def _setup_mock_imports(self):
        """Configure les imports mock pour la simulation"""
        # Mock du module machine pour la simulation
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), "tests"))
        from mock_machine import machine

        sys.modules["machine"] = machine

    def setup_inputs_and_controller(self):
        """Configure les inputs simulés et le contrôleur clavier pour l'émetteur"""
        if self.mode != "emetteur":
            return {}

        from components import SimulatedJoystick
        from keyboard_controller import KeyboardController

        # Créer les joysticks simulés
        inputs = {
            "J1": SimulatedJoystick(36, 39, 32, "J1"),
            "J2": SimulatedJoystick(33, 34, 35, "J2"),
        }

        # Créer et démarrer le contrôleur clavier
        self.keyboard_controller = KeyboardController(inputs)
        self.keyboard_controller.start()

        return inputs

    def setup_mock_pins(self):
        """Configure les pins mockés pour le récepteur"""
        if self.mode != "recepteur":
            return None, None

        # Mock des pins pour simulation
        class MockPin:
            def __init__(self, pin, mode=None):
                self.pin = pin
                self._state = False

            def on(self):
                self._state = True

            def off(self):
                self._state = False

            @property
            def state(self):
                return self._state

        return MockPin(5, None), MockPin(17, None)

    def get_emission_data_template(self) -> Dict:
        """Retourne le template de données pour l'émission"""
        return {
            "message envoyé": False,
            "Joystick J1": "",
            "Joystick J2": "",
        }

    def get_reception_data_template(self) -> Dict:
        """Retourne le template de données pour la réception"""
        return {
            "Statut réception": "En attente",
            "Joystick J1": "Pas de données",
            "Joystick J2": "Pas de données",
            "Moteur 1": "Arrêté",
            "Moteur 2": "Arrêté",
        }

    def get_controls_info_box(self) -> str:
        """Retourne l'info box avec les contrôles clavier"""
        if self.mode != "emetteur":
            return None

        return """🎮 CONTRÔLES CLAVIER:
J1 (gauche): WASD + ESPACE (toggle) + R (centre)
J2 (droite): ↑←↓→ + ENTRÉE (toggle) + C (centre)
Général: Z (tout centrer)"""

    def update_emission_data(self, data: Dict, gamepad_data) -> Dict:
        """Met à jour les données d'émission avec les joysticks"""
        if not self.keyboard_controller:
            return data

        # Envoyer les données
        data["message envoyé"] = self.antenne.send(gamepad_data)

        # Mettre à jour les données des joysticks
        for name, joystick in self.keyboard_controller.joysticks.items():
            if (
                hasattr(joystick, "x")
                and hasattr(joystick, "y")
                and hasattr(joystick, "bt")
            ):
                button_status = "🔴" if joystick.bt == 0 else "⚪"
                data[
                    f"Joystick {name}"
                ] = f"X={joystick.x:4d} Y={joystick.y:4d} {button_status}"

        return data

    def update_reception_data(self, data: Dict, moteur1_pin, moteur2_pin) -> Dict:
        """Met à jour les données de réception"""
        message = self.antenne.receive()

        if isinstance(message, dict):
            data["Statut réception"] = "Données reçues ✓"

            # Adaptation pour les nouvelles données (J1, J2)
            j1_data = message.get("J1")
            if j1_data and len(j1_data) >= 3:
                x, y, btn = j1_data
                button_status = "🔴" if btn == 0 else "⚪"
                data["Joystick J1"] = f"X={x:4d} Y={y:4d} {button_status}"

                if btn == 0:  # Bouton pressé
                    moteur1_pin.off()
                    moteur2_pin.off()
                    data["Moteur 1"] = "Arrêté 🔴"
                    data["Moteur 2"] = "Arrêté 🔴"
                else:
                    moteur1_pin.on()
                    moteur2_pin.on()
                    data["Moteur 1"] = "Marche 🟢"
                    data["Moteur 2"] = "Marche 🟢"

            # Gestion du J2 si présent
            j2_data = message.get("J2")
            if j2_data and len(j2_data) >= 3:
                x2, y2, btn2 = j2_data
                button_status2 = "🔴" if btn2 == 0 else "⚪"
                data["Joystick J2"] = f"X={x2:4d} Y={y2:4d} {button_status2}"
            else:
                data["Joystick J2"] = "Pas de données"

            # Support de l'ancien format pour compatibilité
            x = message.get("X1")
            y = message.get("Y1")
            btn = message.get("Button1")
            if btn is not None and not j1_data:
                if btn == 1:
                    moteur1_pin.off()
                    moteur2_pin.off()
                    data["Moteur 1"] = "Arrêté 🔴"
                    data["Moteur 2"] = "Arrêté 🔴"
                else:
                    moteur1_pin.on()
                    moteur2_pin.on()
                    data["Moteur 1"] = "Marche 🟢"
                    data["Moteur 2"] = "Marche 🟢"
        elif message:
            data["Statut réception"] = f"Données non-dict: {str(message)[:20]}"
        else:
            data["Statut réception"] = "En attente..."

        return data

    def cleanup(self):
        """Nettoie les ressources de la simulation"""
        if self.keyboard_controller:
            self.keyboard_controller.stop()
        if self.antenne and hasattr(self.antenne, "close"):
            self.antenne.close()

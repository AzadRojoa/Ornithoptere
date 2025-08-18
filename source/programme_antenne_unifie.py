"""
Programme principal unifié pour émission et réception
"""
import argparse
import time

# ========== CONFIGURATION ==========
SIMULATION = False  # Mode réel par défaut
ESP32_MODE = "emetteur"  # "emetteur" ou "recepteur" - utilisé quand pas d'arguments CLI
SIMULATION_PORT_EMETTEUR = "/tmp/esp32_emetteur"
SIMULATION_PORT_RECEPTEUR = "/tmp/esp32_recepteur"
# ===================================


def main():
    # Détecter si on est sur ESP32 (pas d'arguments CLI disponibles)
    try:
        import sys

        # Si pas d'arguments ou si on détecte qu'on est sur ESP32
        if len(sys.argv) == 1:
            # Mode ESP32 - utiliser la configuration prédéfinie
            print(f"🔧 MODE ESP32 DÉTECTÉ - {ESP32_MODE.upper()}")
            mode = ESP32_MODE
            simulation_active = SIMULATION
        else:
            # Mode PC avec arguments de ligne de commande
            parser = argparse.ArgumentParser(description="Programme d'antenne unifié")
            parser.add_argument(
                "mode", choices=["emetteur", "recepteur"], help="Mode de fonctionnement"
            )
            parser.add_argument(
                "--simulation", action="store_true", help="Activer le mode simulation"
            )
            args = parser.parse_args()

            # Activer la simulation si demandé
            simulation_active = SIMULATION or args.simulation
            mode = args.mode

    except ImportError:
        # On est probablement sur ESP32, utiliser la config prédéfinie
        print(f"🔧 MODE ESP32 DÉTECTÉ - {ESP32_MODE.upper()}")
        mode = ESP32_MODE
        simulation_active = SIMULATION

    if simulation_active:
        # Mode simulation
        run_simulation_mode(mode)
    else:
        # Mode réel (ESP32)
        run_real_mode(mode)


def run_simulation_mode(mode: str):
    """Lance le programme en mode simulation"""
    from simulation_helper import SimulationHelper
    from tableau_terminal import TableauTerminal

    print(f"🔧 MODE SIMULATION ACTIVÉ - {mode.upper()}")

    # Choisir le bon port selon le mode
    port = SIMULATION_PORT_EMETTEUR if mode == "emetteur" else SIMULATION_PORT_RECEPTEUR
    print(f"Port série: {port}")

    # Initialiser l'helper de simulation
    sim_helper = SimulationHelper(mode, port)

    if mode == "emetteur":
        run_emission_simulation(sim_helper)
    else:
        run_reception_simulation(sim_helper)


def run_real_mode(mode: str):
    """Lance le programme en mode réel (ESP32)"""
    print(f"🔧 MODE RÉEL ACTIVÉ - {mode.upper()}")

    if mode == "emetteur":
        run_emission_real()
    else:
        run_reception_real()


def run_emission_simulation(sim_helper):
    """Lance l'émission en mode simulation"""
    from gamepad import Gamepad
    from tableau_terminal import TableauTerminal

    # Configuration des inputs et contrôleur clavier
    inputs = sim_helper.setup_inputs_and_controller()

    # Données et tableau
    data = sim_helper.get_emission_data_template()
    titre = "émetteur (SIMULATION)"
    info_box = sim_helper.get_controls_info_box()

    # Initialisation
    gamepad = Gamepad(inputs)
    tableau = TableauTerminal(data, titre=titre, info_box=info_box)
    tableau.start()

    try:
        while True:
            # Lire les données du gamepad
            gamepad_data = gamepad.read()

            # Mettre à jour les données via l'helper
            data = sim_helper.update_emission_data(data, gamepad_data)

            # Mettre à jour le tableau
            tableau.data = data
            time.sleep(0.1)

    except KeyboardInterrupt:
        tableau.stop()
        sim_helper.cleanup()
        print("\\nArrêt de l'émission.")


def run_reception_simulation(sim_helper):
    """Lance la réception en mode simulation"""
    from time import sleep

    from tableau_terminal import TableauTerminal

    # Configuration des pins mockées
    moteur1_pin, moteur2_pin = sim_helper.setup_mock_pins()

    # Données et tableau
    data = sim_helper.get_reception_data_template()
    titre = "récepteur (SIMULATION)"

    tableau = TableauTerminal(data, titre=titre)
    tableau.start()

    try:
        while True:
            # Mettre à jour les données via l'helper
            data = sim_helper.update_reception_data(data, moteur1_pin, moteur2_pin)

            # Mettre à jour le tableau
            tableau.data = data
            sleep(0.1)

    except KeyboardInterrupt:
        tableau.stop()
        sim_helper.cleanup()
        print("\\nArrêt de la réception.")


def run_emission_real():
    """Lance l'émission en mode réel (ESP32)"""
    from antenne import Antenne
    from components import Joystick
    from gamepad import Gamepad
    from tableau_terminal import TableauTerminal

    # Configuration des vrais joysticks
    inputs = {"J1": Joystick(36, 39, 32), "J2": Joystick(33, 34, 35)}

    # Données et tableau
    data = {
        "message envoyé": False,
        "Joystick J1": "",
        "Joystick J2": "",
    }

    # Initialisation
    antenne = Antenne(mode="emetteur")
    gamepad = Gamepad(inputs)
    tableau = TableauTerminal(data, titre="émetteur")
    tableau.start()

    try:
        while True:
            gamepad_data = gamepad.read()
            data["message envoyé"] = antenne.send(gamepad_data)

            # Mettre à jour les données des joysticks réels
            for name, joystick in inputs.items():
                if hasattr(joystick, "read"):
                    x, y, bt = joystick.read()
                    button_status = "🔴" if bt == 0 else "⚪"
                    data[f"Joystick {name}"] = f"X={x:4d} Y={y:4d} {button_status}"

            tableau.data = data
            time.sleep(0.1)

    except KeyboardInterrupt:
        tableau.stop()
        print("\\nArrêt de l'émission.")


def run_reception_real():
    """Lance la réception en mode réel (ESP32)"""
    from time import sleep

    from antenne import Antenne
    from machine import Pin
    from tableau_terminal import TableauTerminal

    # Configuration des vrais pins
    moteur1_pin = Pin(5, Pin.OUT)
    moteur2_pin = Pin(17, Pin.OUT)

    # Données et tableau
    data = {
        "Statut réception": "En attente",
        "Joystick J1": "Pas de données",
        "Joystick J2": "Pas de données",
        "Moteur 1": "Arrêté",
        "Moteur 2": "Arrêté",
    }

    antenne = Antenne(mode="recepteur")
    tableau = TableauTerminal(data, titre="récepteur")
    tableau.start()

    try:
        while True:
            message = antenne.receive()

            if isinstance(message, dict):
                data["Statut réception"] = "Données reçues ✓"

                # Traitement des données (même logique que la simulation)
                j1_data = message.get("J1")
                if j1_data and len(j1_data) >= 3:
                    x, y, btn = j1_data
                    button_status = "🔴" if btn == 0 else "⚪"
                    data["Joystick J1"] = f"X={x:4d} Y={y:4d} {button_status}"

                    if btn == 0:
                        moteur1_pin.off()
                        moteur2_pin.off()
                        data["Moteur 1"] = "Arrêté 🔴"
                        data["Moteur 2"] = "Arrêté 🔴"
                    else:
                        moteur1_pin.on()
                        moteur2_pin.on()
                        data["Moteur 1"] = "Marche 🟢"
                        data["Moteur 2"] = "Marche 🟢"

                j2_data = message.get("J2")
                if j2_data and len(j2_data) >= 3:
                    x2, y2, btn2 = j2_data
                    button_status2 = "🔴" if btn2 == 0 else "⚪"
                    data["Joystick J2"] = f"X={x2:4d} Y={y2:4d} {button_status2}"
                else:
                    data["Joystick J2"] = "Pas de données"

            elif message:
                data["Statut réception"] = f"Données non-dict: {str(message)[:20]}"
            else:
                data["Statut réception"] = "En attente..."

            tableau.data = data
            sleep(0.1)

    except KeyboardInterrupt:
        tableau.stop()
        print("\\nArrêt de la réception.")


if __name__ == "__main__":
    main()

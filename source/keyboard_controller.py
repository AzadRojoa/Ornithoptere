"""
Contrôleur clavier pour la simulation des joysticks
"""
import select
import sys
import termios
import threading
import time
import tty
from typing import Callable, Dict, Optional


class KeyboardController:
    """Gestionnaire de clavier pour contrôler les joysticks simulés"""

    def __init__(self, joysticks: Dict[str, any]):
        self.joysticks = joysticks
        self.running = False
        self.thread: Optional[threading.Thread] = None

        # Configuration des touches par défaut
        self.key_mappings = {
            # Joystick J1 (WASD + Espace)
            "w": ("J1", "increment_y", 200),  # Haut
            "s": ("J1", "increment_y", -200),  # Bas
            "a": ("J1", "increment_x", -200),  # Gauche
            "d": ("J1", "increment_x", 200),  # Droite
            " ": ("J1", "toggle_button", None),  # Espace = toggle bouton J1
            # Joystick J2 (Flèches + Enter)
            "\x1b[A": ("J2", "increment_y", 200),  # Flèche haut
            "\x1b[B": ("J2", "increment_y", -200),  # Flèche bas
            "\x1b[D": ("J2", "increment_x", -200),  # Flèche gauche
            "\x1b[C": ("J2", "increment_x", 200),  # Flèche droite
            "\r": ("J2", "toggle_button", None),  # Enter = toggle bouton J2
            # Touches de remise à zéro
            "r": ("J1", "center", None),  # R = centrer J1
            "c": ("J2", "center", None),  # C = centrer J2
            "z": ("ALL", "center", None),  # Z = tout centrer
        }

        # État des touches pour éviter les répétitions
        self.key_pressed = set()
        # État des boutons toggles
        self.button_states = {"J1": False, "J2": False}

        # État original du terminal
        self.old_settings = None

    def start(self):
        """Démarre le contrôleur clavier dans un thread séparé"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._keyboard_loop, daemon=True)
            self.thread.start()
            print("🎮 Contrôleur clavier activé !")
            self._print_help()

    def stop(self):
        """Arrête le contrôleur clavier"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
        self._restore_terminal()

    def _setup_terminal(self):
        """Configure le terminal pour la lecture des touches"""
        if sys.stdin.isatty():
            self.old_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())

    def _restore_terminal(self):
        """Restaure les paramètres originaux du terminal"""
        if self.old_settings:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    def _read_key(self) -> Optional[str]:
        """Lit une touche sans bloquer"""
        try:
            if sys.stdin.isatty():
                if select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], []):
                    key = sys.stdin.read(1)

                    # Gestion des séquences d'échappement (flèches)
                    if key == "\x1b":
                        if select.select([sys.stdin], [], [], 0.1) == (
                            [sys.stdin],
                            [],
                            [],
                        ):
                            key += sys.stdin.read(2)

                    return key
        except Exception:
            pass
        return None

    def _keyboard_loop(self):
        """Boucle principale de lecture du clavier"""
        self._setup_terminal()

        try:
            while self.running:
                key = self._read_key()
                if key:
                    self._process_key(key)
                else:
                    # Nettoyer l'état des touches si aucune touche n'est pressée
                    self.key_pressed.clear()

                time.sleep(0.01)  # Éviter une surcharge CPU

        except Exception as e:
            print(f"Erreur dans la boucle clavier: {e}")
        finally:
            self._restore_terminal()

    def _process_key(self, key: str):
        """Traite une touche pressée"""
        # Éviter les répétitions de touches pour les actions de toggle
        if key in [" ", "\r"] and key in self.key_pressed:
            return

        if key in self.key_mappings:
            joystick_name, action, value = self.key_mappings[key]

            # Marquer la touche comme pressée pour les actions de toggle
            if action == "toggle_button":
                self.key_pressed.add(key)

            if joystick_name == "ALL":
                # Action sur tous les joysticks
                if action == "center":
                    # Centrer tous les joysticks et réinitialiser tous les boutons
                    for name, joy in self.joysticks.items():
                        if hasattr(joy, action):
                            getattr(joy, action)()
                        if name in self.button_states:
                            self.button_states[name] = False
                            if hasattr(joy, "release_button"):
                                joy.release_button()
                else:
                    for joy in self.joysticks.values():
                        if hasattr(joy, action):
                            if value is not None:
                                getattr(joy, action)(value)
                            else:
                                getattr(joy, action)()
            else:
                # Action sur un joystick spécifique
                if joystick_name in self.joysticks:
                    joystick = self.joysticks[joystick_name]

                    if action == "toggle_button":
                        # Gérer le toggle du bouton
                        self._toggle_button(joystick_name, joystick)
                    elif action == "center":
                        # Centrer le joystick et réinitialiser l'état du bouton
                        if hasattr(joystick, action):
                            getattr(joystick, action)()
                        if joystick_name in self.button_states:
                            self.button_states[joystick_name] = False
                            if hasattr(joystick, "release_button"):
                                joystick.release_button()
                    elif hasattr(joystick, action):
                        if value is not None:
                            getattr(joystick, action)(value)
                        else:
                            getattr(joystick, action)()

    def _toggle_button(self, joystick_name: str, joystick):
        """Bascule l'état du bouton d'un joystick"""
        if joystick_name in self.button_states:
            current_state = self.button_states[joystick_name]
            new_state = not current_state
            self.button_states[joystick_name] = new_state

            if new_state:
                # Activer le bouton
                if hasattr(joystick, "press_button"):
                    joystick.press_button()
            else:
                # Désactiver le bouton
                if hasattr(joystick, "release_button"):
                    joystick.release_button()

    def _release_buttons(self):
        """Relâche automatiquement tous les boutons des joysticks"""
        for joystick in self.joysticks.values():
            if hasattr(joystick, "release_button"):
                joystick.release_button()

    def _print_help(self):
        """Affiche l'aide pour les contrôles clavier"""
        print("\n" + "=" * 50)
        print("🎮 CONTRÔLES CLAVIER SIMULATION")
        print("=" * 50)
        print("Joystick J1 (gauche):")
        print("  W/A/S/D    : Déplacer le joystick")
        print("  ESPACE     : Basculer le bouton (ON/OFF)")
        print("  R          : Centrer le joystick")
        print()
        print("Joystick J2 (droite):")
        print("  ↑/←/↓/→    : Déplacer le joystick")
        print("  ENTRÉE     : Basculer le bouton (ON/OFF)")
        print("  C          : Centrer le joystick")
        print()
        print("Général:")
        print("  Z          : Centrer tous les joysticks")
        print("  Ctrl+C     : Quitter")
        print("=" * 50 + "\n")

    def get_joystick_status(self) -> str:
        """Retourne le statut actuel des joysticks pour affichage"""
        status = []
        for name, joystick in self.joysticks.items():
            if (
                hasattr(joystick, "x")
                and hasattr(joystick, "y")
                and hasattr(joystick, "bt")
            ):
                button_status = "🔴" if joystick.bt == 0 else "⚪"
                status.append(
                    f"{name}: X={joystick.x:4d} Y={joystick.y:4d} Btn={button_status}"
                )
        return " | ".join(status)

from typing import Dict, Optional

from components import Moteur, ServoMoteur
from machine import Pin


class FlightControler:
    def __init__(
        self,
        moteur1_pin: int,
        moteur2_pin: int,
        servo1_pin: Optional[int] = None,
        servo2_pin: Optional[int] = None,
    ):
        """
        Initialise le contrôleur de vol avec les pins des moteurs et servomoteurs.
        """
        self.moteur1 = Moteur(moteur1_pin)
        self.moteur2 = Moteur(moteur2_pin)
        self.servo1 = ServoMoteur(servo1_pin) if servo1_pin is not None else None
        self.servo2 = ServoMoteur(servo2_pin) if servo2_pin is not None else None

    def set_motor_speed(self, motor_id: int, speed: int) -> None:
        """Règle la vitesse du moteur spécifié (1 ou 2)."""
        if motor_id == 1:
            self.moteur1.speed = speed
        elif motor_id == 2:
            self.moteur2.speed = speed

    def set_servo_angle(self, servo_id: int, angle: int) -> None:
        """Règle l'angle du servomoteur spécifié (1 ou 2)."""
        if servo_id == 1 and self.servo1:
            self.servo1.deg = angle
        elif servo_id == 2 and self.servo2:
            self.servo2.deg = angle

    def stop_all(self) -> None:
        """Arrête tous les moteurs."""
        self.moteur1.set_speed(0)
        self.moteur2.set_speed(0)
        if self.servo1:
            self.servo1.deg = 0
        if self.servo2:
            self.servo2.deg = 0

    def update_from_dict(self, data: Dict) -> None:
        """Met à jour les moteurs/servos selon un dict reçu."""
        if "motor1" in data:
            self.set_motor_speed(1, data["motor1"])
        if "motor2" in data:
            self.set_motor_speed(2, data["motor2"])
        if "servo1" in data and self.servo1:
            self.set_servo_angle(1, data["servo1"])
        if "servo2" in data and self.servo2:
            self.set_servo_angle(2, data["servo2"])

    def status(self) -> Dict:
        """Retourne l'état courant des moteurs et servos."""
        return {
            "motor1": self.moteur1.speed,
            "motor2": self.moteur2.speed,
            "servo1": self.servo1.deg if self.servo1 else None,
            "servo2": self.servo2.deg if self.servo2 else None,
        }

    def emergency_stop(self) -> None:
        """Arrêt d'urgence de tous les moteurs."""
        self.stop_all()

from typing import Tuple

from machine import ADC, PWM, Pin

# INPUTS


class Joystick:
    def __init__(
        self, pin_x: int, pin_y: int, pin_bt: int, attenuation: int = ADC.ATTN_11DB
    ) -> None:
        self._x: ADC = ADC(Pin(pin_x))
        self._x.atten(attenuation)
        self._y: ADC = ADC(Pin(pin_y))
        self._y.atten(attenuation)
        self._bt: Pin = Pin(pin_bt, Pin.IN, Pin.PULL_UP)

    def read(self) -> Tuple[int, int]:
        return (self._x.read(), self._y.read(), self.bt)

    def __str__(self) -> str:
        return f"Joystick(X={self.x}, Y={self.y}, Button={self.bt})"

    @property
    def x(self) -> int:
        return self._x.read()

    @property
    def y(self) -> int:
        return self._y.read()

    @property
    def bt(self) -> int:
        return self._bt.value()


class SimulatedJoystick:
    """Joystick simulé contrôlable par clavier"""

    def __init__(self, pin_x: int, pin_y: int, pin_bt: int, name: str = ""):
        self.name = name
        self.pin_x = pin_x
        self.pin_y = pin_y
        self.pin_bt = pin_bt

        # Valeurs centrales par défaut (ADC 12 bits: 0-4095, centre à 2048)
        self._x_value = 2048
        self._y_value = 2048
        self._bt_value = 1  # Non pressé par défaut

        # Pas d'incrémentation pour les contrôles
        self.step = 200

        # Limites ADC 12 bits
        self.min_val = 0
        self.max_val = 4095

    def read(self) -> Tuple[int, int, int]:
        return (self._x_value, self._y_value, self._bt_value)

    def set_x(self, value: int) -> None:
        """Définir directement la valeur X"""
        self._x_value = max(self.min_val, min(self.max_val, value))

    def set_y(self, value: int) -> None:
        """Définir directement la valeur Y"""
        self._y_value = max(self.min_val, min(self.max_val, value))

    def increment_x(self, delta: int) -> None:
        """Incrémenter la valeur X"""
        self._x_value = max(self.min_val, min(self.max_val, self._x_value + delta))

    def increment_y(self, delta: int) -> None:
        """Incrémenter la valeur Y"""
        self._y_value = max(self.min_val, min(self.max_val, self._y_value + delta))

    def press_button(self) -> None:
        """Simuler appui sur le bouton"""
        self._bt_value = 0

    def release_button(self) -> None:
        """Simuler relâchement du bouton"""
        self._bt_value = 1

    def center(self) -> None:
        """Remettre le joystick au centre"""
        self._x_value = 2048
        self._y_value = 2048

    @property
    def x(self) -> int:
        return self._x_value

    @property
    def y(self) -> int:
        return self._y_value

    @property
    def bt(self) -> int:
        return self._bt_value

    def __str__(self) -> str:
        return f"SimulatedJoystick({self.name}: X={self.x}, Y={self.y}, Button={'Pressed' if self.bt == 0 else 'Released'})"


class Bouton:
    def __init__(self, pin: int, pull: int = Pin.PULL_UP) -> None:
        self._pin: Pin = Pin(pin, Pin.IN, pull)

    def is_pressed(self) -> bool:
        return self._pin.value() == 0

    def __str__(self) -> str:
        return f"Bouton(pin={self.pin}, value={self.value})"

    @property
    def value(self) -> int:
        return self._pin.value()

    @property
    def pin(self) -> int:
        return self._pin.id()


# OUTPUTS


class ServoMoteur:
    def __init__(
        self, pin: int, freq: int = 50, min_us: int = 500, max_us: int = 2500
    ) -> None:
        self.pwm: PWM = PWM(Pin(pin), freq=freq)
        self.min_us: int = min_us
        self.max_us: int = max_us
        self._angle: int = 0

    def angle(self, deg: int) -> None:
        self._angle = deg
        us: int = self.min_us + (self.max_us - self.min_us) * deg // 180
        duty: int = int(us * 1023 // 20000)
        self.pwm.duty(duty)

    @property
    def frequency(self) -> int:
        return self.pwm.freq()

    @frequency.setter
    def frequency(self, value: int) -> None:
        self.pwm.freq(value)

    @property
    def deg(self) -> int:
        return self._angle

    @deg.setter
    def deg(self, value: int) -> None:
        self.angle(value)


class Moteur:
    def __init__(self, pin: int, freq: int = 1000) -> None:
        self.pwm: PWM = PWM(Pin(pin), freq=freq)
        self._duty: int = 512

    def set_speed(self, value: int) -> None:
        self._duty = int(value * 1023 / 100)
        self.pwm.duty(self._duty)

    @property
    def duty(self) -> int:
        return self._duty

    @duty.setter
    def duty(self, value: int) -> None:
        self._duty = value
        self.pwm.duty(self._duty)

    @property
    def frequency(self) -> int:
        return self.pwm.freq()

    @frequency.setter
    def frequency(self, value: int) -> None:
        self.pwm.freq(value)

    @property
    def speed(self) -> int:
        return round(self._duty * 100 / 1023)

    @speed.setter
    def speed(self, value: int) -> None:
        self.set_speed(value)

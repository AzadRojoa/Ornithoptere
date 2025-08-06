from machine import Pin, ADC, PWM
from typing import Tuple

class Joystick:
    def __init__(self, pin_x: int, pin_y: int, attenuation: int = ADC.ATTN_11DB) -> None:
        self._x: ADC = ADC(Pin(pin_x))
        self._x.atten(attenuation)
        self._y: ADC = ADC(Pin(pin_y))
        self._y.atten(attenuation)

    def read(self) -> Tuple[int, int]:
        return (self._x.read(), self._y.read())

    @property
    def x(self) -> int:
        return self._x.read()

    @property
    def y(self) -> int:
        return self._y.read()

class Bouton:
    def __init__(self, pin: int, pull: int = Pin.PULL_UP) -> None:
        self.pin: Pin = Pin(pin, Pin.IN, pull)

    def is_pressed(self) -> bool:
        return self.pin.value() == 0

    @property
    def value(self) -> int:
        return self.pin.value()

class ServoMoteur:
    def __init__(self, pin: int, freq: int = 50, min_us: int = 500, max_us: int = 2500) -> None:
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
        self.set_speed(value)

    @property
    def frequency(self) -> int:
        return self.pwm.freq()

    @frequency.setter
    def frequency(self, value: int) -> None:
        self.pwm.freq(value)

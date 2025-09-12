from machine import Pin, PWM

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

    @property
    def speed(self) -> int:
        return int(self._duty * 100 / 1023)
    
    @speed.setter
    def speed(self, value: int) -> None:
        self.set_speed(value)

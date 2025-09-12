from machine import Pin, PWM

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

from machine import Pin, ADC, PWM

class Joystick:
    def __init__(self, pin_x, pin_y, attenuation=ADC.ATTN_11DB):
        self._x = ADC(Pin(pin_x))
        self._x.atten(attenuation)
        self._y = ADC(Pin(pin_y))
        self._y.atten(attenuation)

    def read(self):
        return (self._x.read(), self._y.read())
    
    @property
    def x(self):
        return self._x.read()
    
    @property
    def y(self):
        return self._y.read()

class Bouton:
    def __init__(self, pin, pull=Pin.PULL_UP):
        self.pin = Pin(pin, Pin.IN, pull)

    def is_pressed(self):
        return self.pin.value() == 0
    
    @property
    def value(self):
        return self.pin.value()

class ServoMoteur:
    def __init__(self, pin, freq=50, min_us=500, max_us=2500):
        self.pwm = PWM(Pin(pin), freq=freq)
        self.min_us = min_us
        self.max_us = max_us
        self._angle = 0

    def angle(self, deg):
        self._angle = deg
        us = self.min_us + (self.max_us - self.min_us) * deg // 180
        duty = int(us * 1023 // 20000)
        self.pwm.duty(duty)

    @property
    def frequency(self):
        return self.pwm.freq()

    @frequency.setter
    def frequency(self, value):
        self.pwm.freq(value)
    
    @property
    def deg(self):
        return self._angle
    
    @angle.setter
    def deg(self, value):
        self.angle(value)


class Moteur:
    def __init__(self, pin, freq=1000):
        self.pwm = PWM(Pin(pin), freq=freq)
        self._duty = 512

    def set_speed(self, value):
        self._duty = int(value * 1023 / 100)
        self.pwm.duty(self._duty)
    
    @property
    def duty(self):
        return self._duty
    
    @duty.setter
    def duty(self, value):
        self.set_speed(value)

    @property
    def frequency(self):
        return self.pwm.freq()
    
    @frequency.setter
    def frequency(self, value):
        self.pwm.freq(value)

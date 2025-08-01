from machine import Pin, ADC, PWM

class Joystick:
    def __init__(self, pin_x, pin_y, attenuation=ADC.ATTN_11DB):
        self.x = ADC(Pin(pin_x))
        self.x.atten(attenuation)
        self.y = ADC(Pin(pin_y))
        self.y.atten(attenuation)

    def read(self):
        return (self.x.read(), self.y.read())

class Bouton:
    def __init__(self, pin, pull=Pin.PULL_UP):
        self.pin = Pin(pin, Pin.IN, pull)

    def is_pressed(self):
        return self.pin.value() == 0

class ServoMoteur:
    def __init__(self, pin, freq=50, min_us=500, max_us=2500):
        self.pwm = PWM(Pin(pin), freq=freq)
        self.min_us = min_us
        self.max_us = max_us

    def angle(self, deg):
        us = self.min_us + (self.max_us - self.min_us) * deg // 180
        duty = int(us * 1023 // 20000)
        self.pwm.duty(duty)

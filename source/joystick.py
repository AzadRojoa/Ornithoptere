from machine import Pin, ADC
from typing import Tuple

class Joystick:
    def __init__(self, pin_x: int, pin_y: int, pin_bt: int, attenuation: int = ADC.ATTN_11DB) -> None:
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

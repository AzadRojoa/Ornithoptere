from machine import Pin

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

"""
Mock du module machine de MicroPython pour les tests sur Python standard
"""
from unittest.mock import MagicMock


class MockPin:
    IN = 1
    OUT = 0
    PULL_UP = 1
    PULL_DOWN = 0

    def __init__(self, pin_id, mode=None, pull=None):
        self.id_val = pin_id
        self._value = 0

    def value(self, val=None):
        if val is not None:
            self._value = val
        return self._value

    def id(self):
        return self.id_val


class MockADC:
    ATTN_11DB = 3

    def __init__(self, pin):
        self.pin = pin
        self._value = 2048  # Valeur par défaut au centre

    def atten(self, attenuation):
        pass

    def read(self):
        return self._value


class MockPWM:
    def __init__(self, pin, freq=50):
        self.pin = pin
        self._freq = freq
        self._duty = 512

    def freq(self, value=None):
        if value is not None:
            self._freq = value
        return self._freq

    def duty(self, value=None):
        if value is not None:
            self._duty = value
        return self._duty


# Création du mock du module machine
machine = MagicMock()
machine.Pin = MockPin
machine.ADC = MockADC
machine.PWM = MockPWM

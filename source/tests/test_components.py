import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import unittest
from unittest.mock import MagicMock, patch


# Mock classes to replace machine.Pin, ADC, PWM
class MockPin:
    IN = 0
    PULL_UP = 1

    def __init__(self, pin, mode=None, pull=None):
        self._id = pin
        self._value = 1

    def value(self):
        return self._value

    def id(self):
        return self._id


class MockADC:
    ATTN_11DB = 0

    def __init__(self, pin):
        self._pin = pin

    def atten(self, attn):
        pass

    def read(self):
        return 42


class MockPWM:
    def __init__(self, pin, freq=50):
        self._freq = freq
        self._duty = 0

    def duty(self, value):
        self._duty = value

    def freq(self, value=None):
        if value is not None:
            self._freq = value
        return self._freq


with patch.dict(
    "sys.modules", {"machine": MagicMock(Pin=MockPin, ADC=MockADC, PWM=MockPWM)}
):
    from components import Bouton, Joystick, Moteur, ServoMoteur


class TestComponents(unittest.TestCase):
    def test_joystick(self):
        js = Joystick(1, 2, 3)
        self.assertEqual(js.x, 42)
        self.assertEqual(js.y, 42)
        self.assertEqual(js.bt, 1)
        self.assertEqual(js.read(), (42, 42, 1))

    def test_bouton(self):
        bt = Bouton(4)
        self.assertEqual(bt.value, 1)
        self.assertEqual(bt.pin, 4)
        self.assertFalse(bt.is_pressed())

    def test_servomoteur(self):
        sm = ServoMoteur(5)
        sm.angle(90)
        self.assertEqual(sm.deg, 90)
        sm.frequency = 60
        self.assertEqual(sm.frequency, 60)
        sm.deg = 45
        self.assertEqual(sm.deg, 45)

    def test_moteur(self):
        m = Moteur(6)
        m.set_speed(50)
        self.assertEqual(m.speed, 50)
        m.duty = 512
        self.assertEqual(m.duty, 512)
        m.frequency = 2000
        self.assertEqual(m.frequency, 2000)
        m.speed = 75
        self.assertEqual(m.speed, 75)


if __name__ == "__main__":
    unittest.main()

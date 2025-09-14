"""
Mock classes pour simuler les modules hardware de MicroPython
utilisés dans les tests unitaires.
"""
from typing import Any, Optional, Union
from unittest.mock import Mock

class MockPin:
    """Mock pour machine.Pin"""
    IN = 0
    OUT = 1
    PULL_UP = 2
    PULL_DOWN = 3
    
    def __init__(self, pin_id: int, mode: int = 0, pull: int = None):
        self.pin_id = pin_id
        self.mode = mode
        self.pull = pull
        self._value = 1 if pull == self.PULL_UP else 0
    
    def value(self, val: Optional[int] = None) -> int:
        if val is not None:
            self._value = val
        return self._value
    
    def id(self) -> int:
        return self.pin_id

class MockADC:
    """Mock pour machine.ADC"""
    ATTN_11DB = 3
    
    def __init__(self, pin):
        self.pin = pin
        self._value = 2048  # Valeur par défaut au milieu de la plage
    
    def atten(self, attenuation: int):
        pass
    
    def read(self) -> int:
        return self._value
    
    def set_value(self, value: int):
        """Méthode helper pour les tests"""
        self._value = value

class MockPWM:
    """Mock pour machine.PWM"""
    def __init__(self, pin, freq: int = 1000):
        self.pin = pin
        self._freq = freq
        self._duty = 0
    
    def freq(self, frequency: Optional[int] = None) -> int:
        if frequency is not None:
            self._freq = frequency
        return self._freq
    
    def duty(self, duty_cycle: Optional[int] = None) -> int:
        if duty_cycle is not None:
            self._duty = duty_cycle
        return self._duty

class MockSPI:
    """Mock pour machine.SPI"""
    def __init__(self, spi_id: int, baudrate: int = 1000000, 
                 polarity: int = 0, phase: int = 0, 
                 sck=None, mosi=None, miso=None):
        self.spi_id = spi_id
        self.baudrate = baudrate
        self.polarity = polarity
        self.phase = phase
        self.sck = sck
        self.mosi = mosi
        self.miso = miso

class MockNRF24L01:
    """Mock pour le module NRF24L01"""
    def __init__(self, spi, csn, ce, payload_size: int = 32):
        self.spi = spi
        self.csn = csn
        self.ce = ce
        self.payload_size = payload_size
        self._listening = False
        self._messages = []
        self._tx_address = None
        self._rx_addresses = {}
        self._channel = 76
        
    def open_tx_pipe(self, address: bytes):
        self._tx_address = address
    
    def open_rx_pipe(self, pipe: int, address: bytes):
        self._rx_addresses[pipe] = address
    
    def set_power_speed(self, power: int, speed: int):
        pass
    
    def set_channel(self, channel: int):
        self._channel = channel
    
    def start_listening(self):
        self._listening = True
    
    def stop_listening(self):
        self._listening = False
    
    def send(self, data: bytes):
        if not self._listening:
            # Simule l'envoi réussi
            return
        else:
            raise OSError("Cannot send while listening")
    
    def any(self) -> bool:
        return len(self._messages) > 0
    
    def recv(self) -> bytes:
        if self._messages:
            return self._messages.pop(0)
        return b""
    
    def add_message(self, message: bytes):
        """Méthode helper pour les tests"""
        self._messages.append(message)

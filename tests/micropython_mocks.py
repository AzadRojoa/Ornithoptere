"""
Système de mocks pour les modules MicroPython
Ce module doit être importé avant tous les autres pour simuler les modules hardware
"""
import sys
from unittest.mock import MagicMock

# Créer les mocks des modules MicroPython
class MockMachine:
    """Mock pour le module machine"""
    
    class Pin:
        IN = 0
        OUT = 1
        PULL_UP = 2
        PULL_DOWN = 3
        
        def __init__(self, pin_id: int, mode: int = 0, pull: int = None):
            self.pin_id = pin_id
            self.mode = mode
            self.pull = pull
            self._value = 1 if pull == self.PULL_UP else 0
        
        def value(self, val=None):
            if val is not None:
                self._value = val
            return self._value
        
        def id(self):
            return self.pin_id
    
    class ADC:
        ATTN_11DB = 3
        
        def __init__(self, pin):
            self.pin = pin
            self._value = 2048
        
        def atten(self, attenuation):
            pass
        
        def read(self):
            return self._value
    
    class PWM:
        def __init__(self, pin, freq=1000):
            self.pin = pin
            self._freq = freq
            self._duty = 0
        
        def freq(self, frequency=None):
            if frequency is not None:
                self._freq = frequency
            return self._freq
        
        def duty(self, duty_cycle=None):
            if duty_cycle is not None:
                self._duty = duty_cycle
            return self._duty
    
    class SPI:
        def __init__(self, spi_id, baudrate=1000000, polarity=0, phase=0, 
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
    def __init__(self, spi, csn, ce, payload_size=32):
        self.spi = spi
        self.csn = csn
        self.ce = ce
        self.payload_size = payload_size
        self._listening = False
        self._messages = []
        self._tx_address = None
        self._rx_addresses = {}
        self._channel = 76
        
    def open_tx_pipe(self, address):
        self._tx_address = address
    
    def open_rx_pipe(self, pipe, address):
        self._rx_addresses[pipe] = address
    
    def set_power_speed(self, power, speed):
        pass
    
    def set_channel(self, channel):
        self._channel = channel
    
    def start_listening(self):
        self._listening = True
    
    def stop_listening(self):
        self._listening = False
    
    def send(self, data):
        if not self._listening:
            # Simule l'envoi réussi
            return
        else:
            raise OSError("Cannot send while listening")
    
    def any(self):
        return len(self._messages) > 0
    
    def recv(self):
        if self._messages:
            return self._messages.pop(0)
        return b""
    
    def add_message(self, message):
        """Méthode helper pour les tests"""
        self._messages.append(message)

# Mock pour ujson (utilisé dans les modules MicroPython)
class MockUJson:
    @staticmethod
    def dumps(obj):
        import json
        return json.dumps(obj)
    
    @staticmethod
    def loads(s):
        import json
        return json.loads(s)

# Mock pour time (version MicroPython)
class MockTime:
    @staticmethod
    def localtime():
        import time
        t = time.localtime()
        return t

# Mock pour logging (version simplifiée pour MicroPython)
class MockLogging:
    INFO = 20
    DEBUG = 10
    WARNING = 30
    ERROR = 40
    
    @staticmethod
    def basicConfig(level=None):
        pass
    
    @staticmethod
    def getLogger(name):
        return MagicMock()

def setup_micropython_mocks():
    """Configure les mocks des modules MicroPython"""
    # Mock du module machine
    sys.modules['machine'] = MockMachine()
    
    # Mock du module nrf24l01
    nrf_module = MagicMock()
    nrf_module.NRF24L01 = MockNRF24L01
    sys.modules['nrf24l01'] = nrf_module
    
    # Mock de ujson
    sys.modules['ujson'] = MockUJson()
    
    # Mock de time si nécessaire
    if 'time' not in sys.modules:
        sys.modules['time'] = MockTime()
    
    # Mock de logging si nécessaire pour les modules MicroPython
    if 'logging' not in sys.modules:
        sys.modules['logging'] = MockLogging()

# Configurer les mocks dès l'importation
setup_micropython_mocks()

from machine import Pin, SPI, ADC
from lib.nrf24l01 import NRF24L01

class Antenne:
    def __init__(self, mode='emetteur', address=b"2Node", channel=76, payload_size=32, spi_id=1, spi_baudrate=9600, spi_polarity=0, spi_phase=0, sck_pin=18, mosi_pin=23, miso_pin=19, ce_pin=26, csn_pin=27):
        self.mode = mode
        self.address = address
        self.channel = channel
        self.payload_size = payload_size

        self.spi = SPI(spi_id, baudrate=spi_baudrate, polarity=spi_polarity, phase=spi_phase, sck=Pin(sck_pin), mosi=Pin(mosi_pin), miso=Pin(miso_pin))
        self.ce = Pin(ce_pin, Pin.OUT)
        self.csn = Pin(csn_pin, Pin.OUT)

        self.nrf = NRF24L01(self.spi, self.csn, self.ce, payload_size=self.payload_size)

        if self.mode == 'emetteur':
            self.nrf.open_tx_pipe(self.address)
            self.nrf.set_power_speed(0x06, 0x20)
            self.nrf.stop_listening()
            self.nrf.set_channel(self.channel)
        elif self.mode == 'recepteur':
            self.nrf.open_rx_pipe(1, self.address)
            self.nrf.set_channel(self.channel)
            self.nrf.start_listening()
        else:
            raise ValueError("mode must be 'emetteur' or 'recepteur'")

    def send(self, message:str|bytes):
        if self.mode != 'emetteur':
            raise RuntimeError("Cannot send in recepteur mode")
        if isinstance(message, str):
            message = message.encode('utf-8')
        try:
            self.nrf.send(message)
            print("Message reçu (ACK)")
            return True
        except OSError:
            print("Erreur d'envoi (pas d'ACK)")
            return False

    def receive(self):
        if self.mode != 'recepteur':
            raise RuntimeError("Cannot receive in emetteur mode")
        if self.nrf.any():
            return self.nrf.recv().decode('utf-8')
        return None

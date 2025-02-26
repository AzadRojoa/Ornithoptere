from machine import Pin, SPI
from nrf24l01 import NRF24L01
from time import sleep

# Configuration des broches SPI pour l'ESP32
spi = SPI(1, baudrate=9600, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
ce = Pin(26, Pin.OUT)
csn = Pin(27, Pin.OUT)

# Initialisation du module NRF24L01 en mode émetteur
nrf = NRF24L01(spi, csn, ce, payload_size=32)
nrf.open_tx_pipe(b"2Node")  # Adresse de destination
nrf.set_power_speed(0x06, 0x20)  # Puissance max, 250kbps (meilleur pour ESP32)
nrf.stop_listening()  # Mode émetteur
nrf.set_channel(76)

# Message à envoyer
message = b"Bonjour ESP32!"

# Fonction pour envoyer un message
def envoyer_message():
    try:
        nrf.send(message)
        print("Message envoyé :", message.decode())
    except OSError:
        print("Erreur lors de l'envoi")

# Boucle principale
while True:
    envoyer_message()
    sleep(1)  # Pause entre les envois
from machine import Pin, SPI
from nrf24l01 import NRF24L01
from time import sleep
import time

# Configuration des broches
spi = SPI(1, baudrate=9600, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
ce = Pin(26, Pin.OUT)
csn = Pin(27, Pin.OUT)

# Initialisation du module NRF24L01 en mode récepteur
nrf = NRF24L01(spi, csn, ce, payload_size=32)
nrf.open_rx_pipe(1, b"2Node")  # Adresse du récepteur
#nrf.open_rx_pipe(1, b"\x11\x11\x11\x11\x11")
nrf.set_channel(76)
nrf.start_listening()

# Fonction pour écouter les messages reçus
def recevoir_message():
    if nrf.any():
        try:
            message = nrf.recv()
            print(f"Message reçu : {message}")
            print(time.gmtime()[5] )
            #print(str(time.gmtime()[3]) + "h "+ str(time.gmtime()[4]) + "min " + str(time.gmtime()[5] + "sec")
        except OSError:
            print("Erreur lors de la réception")


# Boucle principale
while True:
    recevoir_message()
    sleep(0.1)  # Petite pause pour éviter de bloquer la boucle


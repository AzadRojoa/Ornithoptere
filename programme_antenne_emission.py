from machine import Pin, SPI, ADC
from nrf24l01 import NRF24L01
from time import sleep
import time

# Configuration des broches SPI pour l'ESP32
spi = SPI(1, baudrate=9600, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
ce = Pin(26, Pin.OUT)
csn = Pin(27, Pin.OUT)

# Configuration des broches ADC et du bouton 1
x1Axis = ADC(Pin(34)) # créer un objet ADC agissant sur une broche avec la pin 34 pour position x
x1Axis.atten(ADC.ATTN_11DB)
y1Axis = ADC(Pin(35)) # créer un objet ADC agissant sur une broche avec la pin 35 pour position y
y1Axis.atten(ADC.ATTN_11DB)
button1 = Pin(33, Pin.IN, Pin.PULL_UP)# broche SW 

# Configuration des broches ADC et du bouton 1
x2Axis = ADC(Pin(36)) # créer un objet ADC agissant sur une broche avec la pin 34 pour position x
x2Axis.atten(ADC.ATTN_11DB)
y2Axis = ADC(Pin(39)) # créer un objet ADC agissant sur une broche avec la pin 35 pour position y
y2Axis.atten(ADC.ATTN_11DB)
button2 = Pin(32, Pin.IN, Pin.PULL_UP)# broche SW

# Initialisation du module NRF24L01 en mode émetteur
nrf = NRF24L01(spi, csn, ce, payload_size=32)
nrf.open_tx_pipe(b"2Node")  # Adresse de destination
nrf.set_power_speed(0x06, 0x20)  # Puissance max, 250kbps (meilleur pour ESP32)
nrf.stop_listening()  # Mode émetteur
nrf.set_channel(76)

# Fonction pour envoyer un message
def envoyer_message(message):
    try:
        nrf.send(message)
        print("Message envoyé :", message.decode())
        return True
    except OSError as e:
        print("Erreur lors de l'envoi",e)
        return False

# Boucle principale
while True :
    x1Value = x1Axis.read()  # lire une valeur analogique brute dans la plage 0-4095
    y1Value = y1Axis.read()  # lire une valeur analogique brute
    btn1Value = button1.value() # lire la valeur du bouton nommination
    message1 = f"X1:{x1Value}, Y1:{y1Value}, Button1:{btn1Value}".encode('utf-8')  # créer le message à envoyer
    #print(f"X1:{x1Axis.read()}, {message.decode()}")  # imprimer les valeurs pour débogage
    envoyer_message(message1)  # envoyer le message1
    
    if envoyer_message(message1):
        #time.sleep(1)# Pause entre les envois
        x2Value = x2Axis.read()  # lire une valeur analogique brute dans la plage 0-4095
        y2Value = y2Axis.read()  # lire une valeur analogique brute
        btn2Value = button2.value() # lire la valeur du bouton nommination
        message2 = f"X2:{x2Value}, Y2:{y2Value}, Button2:{btn2Value}".encode('utf-8')  # créer le message à envoyer
        #print(f"X2:{x2Axis.read()}, {message.decode()}")  # imprimer les valeurs pour débogage
        envoyer_message(message2)  # envoyer le message2
        
    time.sleep(0.01)  # Pause entre les envois de boucle

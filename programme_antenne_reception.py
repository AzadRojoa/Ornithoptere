from machine import Pin, SPI
from lib.nrf24l01 import NRF24L01
from time import sleep
import ujson

# Configuration SPI et NRF24L01
spi = SPI(1, baudrate=115200, polarity=0, phase=0, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
ce = Pin(26, Pin.OUT)
csn = Pin(27, Pin.OUT)
nrf = NRF24L01(spi, csn, ce, payload_size=32)

# Configuration de l'adresse et du canal
nrf.open_rx_pipe(1, b"2Node")
nrf.set_channel(76)
nrf.start_listening()

buffer = b""  # Stocke les morceaux du message

#Configuration des pins du moteur
moteur_pin = Pin(5, Pin.OUT)

def recevoir_paquets():
    global buffer
    if nrf.any():
        try:
            data = nrf.recv().rstrip(b'\x00')  # Supprime les padding inutiles
            # Convertir les données reçues en chaîne et afficher la valeur brute
            chunk = str(data)
            print(f"Données reçues brutes : {chunk}")
            #chunk = chunk.split("'")[1]
            #print(chunk.split(",")[0])
            #print(chunk.split(",")[1])
            #print(chunk.split(",")[2])
            
             # Supprimer les caractères non numériques ou inutiles
            chunk_clean = chunk.replace("b'", "").replace("X1:", "").replace("X2:", "").replace("Y1:", "").replace("Y2:", "").replace("Button1:", "").replace("Button2:", "").replace("'", "").strip()
            print(f"Données après nettoyage : {chunk_clean}")
            
            #Diviser le message par des virgules
            valeurs = chunk_clean.split(",")
            
            if len(valeurs) == 3:
                #Afficher les trois valeurs du message
                #print(valeurs[0])
                #print(valeurs[1])
                #print(valeurs[2])            
                
                try:
                    valeur_3 = int(valeurs[1].strip())# Supprimer les espaces avant conversion
                    
                    if valeur_3 == 4095:
                        print("Demande d'arrêt du moteur")
                        moteur_pin.off()
        
                    if valeur_3 == 0:
                        print("Demande de marche du moteur")
                        moteur_pin.on()
            
                    else :
                        print("Valeur ne correspond ni à 4095 ni à 0.")
                    
                except ValueError:
                    print(f"Valeur invalide : {valeurs[1]} n'est pas un entier.")
                
        except OSError as e:
            print(f"Erreur de réception : {e}")   

while True:
    recevoir_paquets()
    sleep(0.01)

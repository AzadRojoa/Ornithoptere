from antenne import Antenne
from machine import Pin
from time import sleep

antenne = Antenne(mode='recepteur')
moteur1_pin = Pin(5, Pin.OUT)
moteur2_pin = Pin(17, Pin.OUT)

def reception_paquets() -> None:
    message = antenne.receive()
    if isinstance(message, dict):
        print(f"Données reçues : {message}")
        x = message.get("X1")
        y = message.get("Y1")
        btn = message.get("Button1")
        if btn is not None:
            if btn == 1:
                print("Demande d'arrêt du moteur")
                moteur1_pin.off()
                moteur2_pin.off()
            else:
                print("Demande de marche du moteur")
                moteur1_pin.on()
                moteur2_pin.on()
    elif message:
        print(f"Données reçues non dict : {message}")

while True:
    reception_paquets()



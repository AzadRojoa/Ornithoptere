from antenne import Antenne
from machine import Pin
from time import sleep

antenne = Antenne(mode='recepteur')
moteur1_pin = Pin(5, Pin.OUT)
moteur2_pin = Pin(17, Pin.OUT)

def reception_paquets() -> None:
    message = antenne.receive()
    if message:
        chunk = str(message)
        print(f"Données reçues brutes : {chunk}")
        chunk_clean = (
            chunk.replace("b'", "")
            .replace("X1:", "")
            .replace("X2:", "")
            .replace("Y1:", "")
            .replace("Y2:", "")
            .replace("Button1:", "")
            .replace("Button2:", "")
            .replace("'", "")
            .strip()
        )
        print(f"Données après nettoyage : {chunk_clean}")
        valeurs = chunk_clean.split(",")
        if len(valeurs) == 3:
            try:
                valeur_3 = int(valeurs[1].strip())
                if valeur_3 == 4095:
                    print("Demande d'arrêt du moteur")
                    moteur1_pin.off()
                    moteur2_pin.off()
                else:
                    print("Demande de marche du moteur")
                    moteur1_pin.on()
                    moteur2_pin.on()
            except ValueError:
                print(f"Valeur invalide : {valeurs[1]} n'est pas un entier.")

while True:
    reception_paquets()



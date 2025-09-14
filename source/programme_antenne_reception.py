from antenne import Antenne
from moteur import Moteur
from time import sleep
import math

antenne = Antenne(mode='recepteur')
moteur1 = Moteur(5)
moteur2 = Moteur(17)

moteur_actif = False
bouton_precedent = 0

def reception_paquets() -> None:
    global moteur_actif, bouton_precedent
    
    message = antenne.receive()
    if isinstance(message, dict):
        print(f"Données reçues : {message}")
        x = message.get("X1", 0)
        y = message.get("Y1", 0)
        btn = message.get("Button1", 0)
        
        if btn == 1 and bouton_precedent == 0:
            moteur_actif = not moteur_actif
            print(f"Moteur {'activé' if moteur_actif else 'désactivé'}")
        
        bouton_precedent = btn
        
        if moteur_actif:
            magnitude = math.sqrt(x*x + y*y)
            vitesse = min(int(magnitude), 100)
            
            print(f"Position joystick: X={x}, Y={y}, Vitesse calculée: {vitesse}%")
            
            moteur1.speed = vitesse
            moteur2.speed = vitesse
        else:
            moteur1.speed = 0
            moteur2.speed = 0
            
    elif message:
        print(f"Données reçues non dict : {message}")

while True:
    reception_paquets()
    sleep(0.01)



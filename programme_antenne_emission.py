from antenne import Antenne
from components import Joystick, Bouton
import time

J = Joystick(36, 39)
BT = Bouton(32)

antenne = Antenne(mode='emetteur')

def envoyer_message(message):
    try:
        antenne.send(message)
        print("Message envoyé :", message.decode())
        return True
    except OSError as e:
        print("Erreur lors de l'envoi", e)
        return False

while True:
    x, y = J.read()
    btnValue = BT.pin.value()
    message1 = f"X1:{x}, Y1:{y}, Button1:{btnValue}".encode('utf-8')
    envoyer_message(message1)
        
    time.sleep(0.01)
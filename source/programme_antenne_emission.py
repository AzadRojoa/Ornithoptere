from antenne import Antenne
from components import Joystick, Bouton
import time

J = Joystick(36, 39, 32)

antenne = Antenne(mode='emetteur')

def envoyer_message(message) -> bool:
    result = antenne.send(message)
    if result:
        print(f"Message envoyé : {message}")
    else:
        print("Erreur lors de l'envoi")
    return result

while True:
    x, y, btn_value = J.read()
    message1 = {"X1": x, "Y1": y, "Button1": btn_value}
    envoyer_message(message1)
    time.sleep(0.01)
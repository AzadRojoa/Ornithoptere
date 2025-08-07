from antenne import Antenne
from components import Joystick, Bouton
import time
from tableau_terminal import TableauTerminal
from gamepad import Gamepad

inputs = {
    "J1": Joystick(36, 39, 32),
    "J2": Joystick(33, 34, 35)
}

data = {
    "Nom": "emetteur",
    "message envoyé": False,
    "Message": "Coucou, ceci est un texte long"
}

antenne = Antenne(mode='emetteur')
gamepad = Gamepad(inputs)
tableau = TableauTerminal(data)
tableau.start()

try:
    while True:
        data["message envoyé"] = antenne.send(gamepad.read())
        tableau.data = data
        time.sleep(0.5)
except KeyboardInterrupt:
    tableau.stop()
    print("\nArrêt du test.")
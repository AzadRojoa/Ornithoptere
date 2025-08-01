from lib.antenne import Antenne
from lib.components import Joystick, Bouton
import time

joystick1 = Joystick(34, 35)
button1 = Bouton(33)
joystick2 = Joystick(36, 39)
button2 = Bouton(32)

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
    x1Value, y1Value = joystick1.read()
    btn1Value = button1.pin.value()
    message1 = f"X1:{x1Value}, Y1:{y1Value}, Button1:{btn1Value}".encode('utf-8')
    envoyer_message(message1)
    
    if envoyer_message(message1):
        x2Value, y2Value = joystick2.read()
        btn2Value = button2.pin.value()
        message2 = f"X2:{x2Value}, Y2:{y2Value}, Button2:{btn2Value}".encode('utf-8')
        envoyer_message(message2)
        
    time.sleep(0.01)
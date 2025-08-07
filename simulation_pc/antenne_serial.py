"""
Version simulée de l'antenne utilisant la communication série pour les tests sur PC
"""
import json
import logging
import queue
import threading
import time
from typing import Dict, Optional, Union

import serial

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AntenneSerial:
    """
    Version simulée de la classe Antenne utilisant la communication série
    pour tester sur PC au lieu du NRF24L01
    """

    @property
    def mode(self) -> str:
        """Mode de fonctionnement ('emetteur' ou 'recepteur')."""
        return self._mode

    def __init__(
        self,
        mode: str = "emetteur",
        port: str = "/dev/ttyUSB0",
        baudrate: int = 115200,
        timeout: float = 1.0,
    ) -> None:
        """
        Initialise l'antenne série en mode émetteur ou récepteur.

        Args:
            mode: 'emetteur' ou 'recepteur'
            port: Port série à utiliser (ex: '/dev/ttyUSB0', 'COM3')
            baudrate: Vitesse de communication série
            timeout: Timeout pour les opérations série
        """
        if mode not in ("emetteur", "recepteur"):
            raise ValueError("mode must be 'emetteur' or 'recepteur'")

        self._mode: str = mode
        self._port: str = port
        self._baudrate: int = baudrate
        self._timeout: float = timeout

        # Queue pour les messages reçus
        self._receive_queue = queue.Queue()
        self._serial_connection = None
        self._running = False
        self._thread = None

        self._init_serial()

    def _init_serial(self) -> None:
        """Initialise la connection série"""
        try:
            self._serial_connection = serial.Serial(
                port=self._port, baudrate=self._baudrate, timeout=self._timeout
            )
            logger.info(
                f"Connexion série ouverte sur {self._port} à {self._baudrate} bauds"
            )

            if self._mode == "recepteur":
                self._start_receiver_thread()

        except serial.SerialException as e:
            logger.error(f"Erreur d'ouverture du port série {self._port}: {e}")
            raise

    def _start_receiver_thread(self) -> None:
        """Démarre le thread de réception pour le mode récepteur"""
        self._running = True
        self._thread = threading.Thread(target=self._receiver_loop, daemon=True)
        self._thread.start()
        logger.info("Thread de réception démarré")

    def _receiver_loop(self) -> None:
        """Boucle de réception des messages"""
        while self._running:
            try:
                if self._serial_connection and self._serial_connection.in_waiting > 0:
                    line = self._serial_connection.readline()
                    if line:
                        message = line.decode("utf-8").strip()
                        if message:
                            self._receive_queue.put(message)
            except Exception as e:
                logger.error(f"Erreur dans la boucle de réception: {e}")
            time.sleep(0.01)  # Évite la surcharge CPU

    def send(self, message: Union[str, bytes, Dict]) -> bool:
        """
        Envoie un message via la connexion série (mode émetteur uniquement).

        Args:
            message: Message à envoyer (str, bytes ou dict)

        Returns:
            True si l'envoi a réussi, False sinon
        """
        if self._mode != "emetteur":
            raise RuntimeError("Cannot send in recepteur mode")

        if not self._serial_connection:
            logger.error("Connexion série non disponible")
            return False

        try:
            # Conversion du message en string
            if isinstance(message, dict):
                message_str = "J" + json.dumps(message)
            elif isinstance(message, bytes):
                message_str = message.decode("utf-8")
            else:
                message_str = str(message)

            # Ajout du terminateur de ligne
            message_with_newline = message_str + "\n"

            # Envoi via série
            self._serial_connection.write(message_with_newline.encode("utf-8"))
            self._serial_connection.flush()

            logger.debug(f"Message envoyé: {message_str}")
            return True

        except Exception as e:
            logger.error(f"Erreur d'envoi: {e}")
            return False

    def receive(self) -> Optional[Union[str, dict]]:
        """
        Reçoit un message via la connexion série (mode récepteur uniquement).

        Returns:
            Message reçu (str ou dict) ou None si rien n'est reçu
        """
        if self._mode != "recepteur":
            raise RuntimeError("Cannot receive in emetteur mode")

        try:
            # Récupération non-bloquante d'un message
            message = self._receive_queue.get_nowait()

            # Si le message commence par 'J', c'est du JSON
            if message.startswith("J"):
                try:
                    return json.loads(message[1:])
                except json.JSONDecodeError as e:
                    logger.error(f"Erreur de décodage JSON: {e}")
                    return None
            else:
                return message

        except queue.Empty:
            return None
        except Exception as e:
            logger.error(f"Erreur de réception: {e}")
            return None

    def close(self) -> None:
        """Ferme la connexion série et arrête les threads"""
        self._running = False

        if self._thread:
            self._thread.join(timeout=2.0)

        if self._serial_connection:
            self._serial_connection.close()
            logger.info("Connexion série fermée")

    def __del__(self) -> None:
        """Destructeur pour nettoyer les ressources"""
        self.close()

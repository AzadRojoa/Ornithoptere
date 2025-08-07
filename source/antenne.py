import logging
from typing import Dict, Optional, Union

import ujson
from machine import ADC, SPI, Pin
from nrf24l01 import NRF24L01

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Antenne:
    """
    Classe pour gérer la communication via le module NRF24L01.
    Peut être configurée en mode 'emetteur' ou 'recepteur'.
    """

    @property
    def mode(self) -> str:
        """Mode de fonctionnement ('emetteur' ou 'recepteur')."""
        return self._mode

    def __init__(
        self,
        mode: str = "emetteur",
        address: bytes = b"2Node",
        channel: int = 76,
        payload_size: int = 32,
        spi_id: int = 1,
        spi_baudrate: int = 9600,
        spi_polarity: int = 0,
        spi_phase: int = 0,
        sck_pin: int = 18,
        mosi_pin: int = 23,
        miso_pin: int = 19,
        ce_pin: int = 26,
        csn_pin: int = 27,
    ) -> None:
        """
        Initialise l'antenne en mode émetteur ou récepteur.
        """
        if mode not in ("emetteur", "recepteur"):
            raise ValueError("mode must be 'emetteur' or 'recepteur'")
        self._mode: str = mode
        self._address: bytes = address
        self._channel: int = channel
        self._payload_size: int = payload_size

        self.spi: SPI = SPI(
            spi_id,
            baudrate=spi_baudrate,
            polarity=spi_polarity,
            phase=spi_phase,
            sck=Pin(sck_pin),
            mosi=Pin(mosi_pin),
            miso=Pin(miso_pin),
        )
        self.ce: Pin = Pin(ce_pin, Pin.OUT)
        self.csn: Pin = Pin(csn_pin, Pin.OUT)

        self.nrf: NRF24L01 = NRF24L01(
            self.spi, self.csn, self.ce, payload_size=self._payload_size
        )

        if self._mode == "emetteur":
            self.nrf.open_tx_pipe(self._address)
            self.nrf.set_power_speed(0x06, 0x20)
            self.nrf.stop_listening()
            self.nrf.set_channel(self._channel)
        else:
            self.nrf.open_rx_pipe(1, self._address)
            self.nrf.set_channel(self._channel)
            self.nrf.start_listening()

    def send(self, message: Union[str, bytes, Dict]) -> bool:
        """
        Envoie un message via l'antenne (mode émetteur uniquement).
        Accepte str, bytes ou dict. Les dict sont encodés en JSON avec identifiant 'J'.
        Retourne True si ACK reçu, False sinon.
        """
        if self._mode != "emetteur":
            raise RuntimeError("Cannot send in recepteur mode")
        if isinstance(message, dict):
            message = b"J" + ujson.dumps(message).encode("utf-8")
        elif isinstance(message, str):
            message = message.encode("utf-8")
        try:
            self.nrf.send(message)
            # logger.info("Message reçu (ACK)")
            return True
        except OSError:
            logger.error("Erreur d'envoi (pas d'ACK)")
            return False

    def receive(self) -> Optional[Union[str, dict]]:
        """
        Reçoit un message via l'antenne (mode récepteur uniquement).
        Si le message commence par 'J', le décode en dict (JSON).
        Retourne le message décodé (str ou dict) ou None si rien n'est reçu.
        """
        if self._mode != "recepteur":
            raise RuntimeError("Cannot receive in emetteur mode")
        if self.nrf.any():
            raw = self.nrf.recv()
            if raw.startswith(b"J"):
                try:
                    return ujson.loads(raw[1:].decode("utf-8"))
                except Exception as e:
                    logger.error(f"Erreur de décodage JSON: {e}")
                    return None
            else:
                return raw.decode("utf-8")
        return None

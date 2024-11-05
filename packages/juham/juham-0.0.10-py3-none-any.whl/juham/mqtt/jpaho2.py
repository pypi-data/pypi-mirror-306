# from typing import override
import time
import paho.mqtt.client as paho
import os

from juham.base import JMqtt


class JPaho2(paho.Client, JMqtt):
    """MQTT broker implementation based on paho.mqtt Python package.
    Uses multi-inheritance by subclassing paho.CLient and JMqtt super classes.
    """

    configured: bool = False
    paho_version: int = 2
    _client_ids: set = set()

    @classmethod
    def register_client_id(cls, name_pid: str) -> None:
        if name_pid in cls._client_ids:
            raise ValueError(f"Duplicate MQTT client ID detected: {name_pid}")
        cls._client_ids.add(name_pid)

    def __init__(self, name: str = "paho") -> None:
        # Create a unique client ID
        name_pid = f"{name}_{os.getpid()}_{int(time.time())}"
        self.register_client_id(name_pid)

        # Initialize the base class with the proper protocol argument
        if self.paho_version == 2:
            super().__init__(client_id=name_pid, protocol=paho.MQTTv311)
        else:
            super().__init__(client_id=name_pid)

        self.name = name_pid

    # @override
    def connect_to_server(
        self, host: str = "localhost", port: int = 1883, keepalive: int = 60
    ):
        # FIXME: is this a bug in the new paho version 2? Subclassing paho client with the
        # new paho version 2 throws invalid host
        # exception even if the host is perfectly ok. Worked fine with the previous paho release.
        # The problem is that the private _host instance variable don't get set but is empty
        # even if self.host is set to perfectly valid value. So we set self._host = self.host, which fixes paho client.
        if self._host != host:
            self._host = host
        return super().connect_to_server(host, port, keepalive)

    # def on_message(self, mth):
    #    self.on_message = mth

    # def on_connect(self, mth):
    #    self.on_connect = mth

    # def on_disconnect(self, mth):
    #    self.on_disconnect = mth

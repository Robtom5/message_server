from .defaults import *

class MessageSender():
    def __init__(
            self,
            socket,
            server=DEFAULT_UDP_IP_ADDRESS, 
            port=DEFAULT_UDP_PORT_NO, 
            serialiser = DEFAULT_SERIALISER):
        self._socket = socket
        self.update_target(server, port)
        self._serialise = serialiser

    def send(self, message):
        self._socket.sendto(self._serialise(message), self._target)

    def update_target(self, server, port):
        self._target = (server, port)


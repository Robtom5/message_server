#! /usr/bin/env python3
import pickle
import queue
import socket
import threading
from .server_messages import ServerStatusMessage
from .defaults import *

# look at https://stackoverflow.com/questions/47391774/python-send-and-receive-objects-through-sockets
# for serialising and deserialising using pickle
class MessageServer(threading.Thread):
    def __init__(
            self, 
            serverSocket,
            host=DEFAULT_UDP_IP_ADDRESS, 
            port=DEFAULT_UDP_PORT_NO, 
            controlQueue = queue.Queue(), 
            outputQueue = queue.Queue(),
            serialiser = DEFAULT_SERIALISER,
            deserialiser = DEFAULT_DESERIALISER):
        threading.Thread.__init__(self)
        self.socket = serverSocket
        self.socket.bind((host, port))
        self.socket.settimeout(0.5)
        self._control_queue = controlQueue
        self._output_queue = outputQueue
        self._thread = None
        self.serialise = serialiser
        self.deserialise = deserialiser
        self.isRunning = False

    def _control_message(self, msg):
        self._control_queue.put(msg)

    def close(self):
        self._control_message('exit')

    def status(self):
        if not self.isRunning:
            self._output_queue.put(ServerStatusMessage(False))
        else:
            self._control_message('status')

    def run(self):
        if not self.isRunning:
            self.isRunning = True
            while True:
                try: 
                    msg = self._control_queue.get(False)
                    if msg.lower() == 'exit':
                        self.socket.close()
                        self.isRunning = False
                        self._output_queue.put(ServerStatusMessage(False))
                        break
                    elif msg.lower() == 'status':
                        self._output_queue.put(ServerStatusMessage(True))
                except queue.Empty:
                    pass

                # Server is configured to have a timeout for receiving of 0.5 seconds
                # If this time is reached in the reciev command then a timeout 
                # exception occurs. This allows us to still control everything
                try:
                    # This currently works for small message sizes but will need
                    # to use a loop that concatenates the data and then run list.join
                    # if messages need to get larger
                    (raw, address) = self.socket.recvfrom(4096)
                    # Currently this relies on pickle to serialise and deserialise
                    # but if i want to make a cross platform app i will need to define
                    # serialisation myself
                    data = self.deserialise(raw)
                    print(f"Message received from {address}, type{data}")
                    self._output_queue.put((data, address))
                except socket.timeout:
                    pass


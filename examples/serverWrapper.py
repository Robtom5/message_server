#! /usr/bin/env python3
import message_server as MS
import queue
from dataTypes import *
# import sender

control_queue = queue.Queue()
message_queue = queue.Queue()

server = MS.MessageServer(controlQueue=control_queue, outputQueue=message_queue)
server.start()

while True:
    try:
        msg = message_queue.get(True)
        print(msg)
    except KeyboardInterrupt:
        control_queue.put('exit')
        break
import socket
import message_server as MS
from dataTypes import *


port = MS.DEFAULT_UDP_PORT_NO
serv = MS.DEFAULT_UDP_IP_ADDRESS
prep = MS.DEFAULT_SERIALISER

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = DummyData(4)
sock.sendto(prep(data), (serv, port))
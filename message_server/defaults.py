#! /usr/bin/env python3
import pickle

DEFAULT_UDP_IP_ADDRESS = "127.0.0.1"
DEFAULT_UDP_PORT_NO = 6789
DEFAULT_SERIALISER = lambda data : pickle.dumps(data)
DEFAULT_DESERIALISER = lambda raw : pickle.loads(raw)
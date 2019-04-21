#! /usr/bin/env python3
import pytest
import message_server as MS
import queue
import time
import socket

@pytest.fixture(scope='function')
def inQueue():
    inQueue = queue.Queue()
    yield inQueue

@pytest.fixture(scope='function')
def outQueue():
    outQueue = queue.Queue()
    yield outQueue

@pytest.fixture(scope='function')
def testServer(inQueue, outQueue):
    test_server = MS.MessageServer(controlQueue=inQueue, outputQueue=outQueue)
    yield test_server
    test_server.close()

class DummyData():
    def __init__(self, value):
        self.value = value


def test_init(testServer):
    assert isinstance(testServer, MS.MessageServer)

def test_close_putsExitInQueue(inQueue, testServer):
    assert inQueue.empty()
    testServer.close()
    assert not inQueue.empty()
    assert inQueue.get() == 'exit'

def test_close_closesRunningServer(outQueue, testServer):
    assert outQueue.empty()
    testServer.start()
    testServer.status()

    count = 0
    while outQueue.empty() and count < 5:
        count += 1
        time.sleep(0.5)

    assert not outQueue.empty()
    assert outQueue.get().running == True
    testServer.close()
    while outQueue.empty() and count < 5:
        count += 1
        time.sleep(0.5)
    assert not outQueue.empty()
    assert outQueue.get().running == False

def test_status_generatesMessageWhenServerNotRunning(outQueue, testServer):
    assert outQueue.empty()
    testServer.status()
    assert not outQueue.empty()
    assert outQueue.get().running == False

def test_serverReceivesData(outQueue, testServer):
    assert outQueue.empty()
    testServer.start()
    testServer.status()
    count = 0
    while outQueue.empty() and count < 5:
        count += 1
        time.sleep(0.5)
    else:
        count = 0

    assert not outQueue.empty()
    assert outQueue.get().running == True
    assert outQueue.empty()


    port = MS.DEFAULT_UDP_PORT_NO
    serv = MS.DEFAULT_UDP_IP_ADDRESS
    prep = MS.DEFAULT_SERIALISER
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = DummyData(4)
    sock.sendto(prep(data), (serv, port))

    while outQueue.empty() and count < 5:
        count += 1
        time.sleep(0.5)

    assert not outQueue.empty()
    data = outQueue.get()[0]
    assert isinstance(data, DummyData)
    assert data.value == 4


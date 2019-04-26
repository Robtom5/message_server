#! /usr/bin/env python3
import pytest
import message_server as MS
import socket

def DummySerialiser(message):
    return ""

class DummySocket():
    methodCalled = False
    def sendto(self, message, target):
        self.methodCalled = True

@pytest.fixture(scope='function')
def testSocket():
    test_socket = DummySocket()
    yield test_socket

@pytest.fixture(scope='function')
def testSender(testSocket):
    test_sender = MS.MessageSender(testSocket, serialiser = DummySerialiser)
    yield test_sender

def test_init(testSender):
    assert isinstance(testSender, MS.MessageSender)

def test_update_target_changestargetserver(testSender):
    (oldServer, oldPort) = testSender._target
    newServer = oldServer + "new"
    newPort = oldPort + 1

    testSender.update_target(newServer, newPort)
    (updatedServer, updatedPort) = testSender._target
    assert updatedServer == newServer
    assert updatedPort == newPort

def test_send_shouldsendmessage(testSocket, testSender):
    testSender.send("Test")
    assert testSocket.methodCalled
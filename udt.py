#!/usr/bin/python

# use socket library for portability
import socket as socketlib
from _udt import *
import _udt


class UDTSTATUS(object):
    INIT = 1
    OPENED = 2
    LISTENING = 3
    CONNECTING = 4
    CONNECTED = 5
    BROKEN = 6
    CLOSING = 7
    CLOSED = 8
    NONEXIST = 9


class socket(_udt.socket):
    def connect(self, addr):
        conn_addr = self._get_addr(addr)
        return _udt.socket.connect(self, conn_addr)

    def bind(self, addr):
        bind_addr = self._get_addr(addr)
        return _udt.socket.bind(self, bind_addr)

    def _get_addr(self, (host, port)):
        family, socktype, proto, name, addr = socketlib.getaddrinfo(
            host,
            port,
            self.family,
            socketlib.SOCK_STREAM,
            self.proto,
            0
        )[0]
        return addr


class epoll(_udt.epoll):
    def __init__(self):
        _udt.epoll.__init__(self)
        self._released = False

    def release(self):
        if not self._released:
            _udt.epoll.release(self)

    def add_usock(self, s, events):
        # according to the docs, adding flags is not supported
        rv = _udt.epoll.add_usock(self, s, events)
        return rv

    def add_ssock(self, s, events):
        rv = _udt.epoll.add_ssock(self, s, events)
        return rv

    def remove_usock(self, s):
        rv = _udt.epoll.remove_usock(self, s)
        return rv

    def remove_ssock(self, s):
        rv = _udt.epoll.remove_ssock(self, s)
        return rv

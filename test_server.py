#!/usr/bin/env python
import udt
import socket
from threading import Thread
import logging
import logging.config
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
threads = 10
max_bandwidth = 1024 * 512 * 10


def test(client, text):
    data = "a" * int(text)
    sent = 0
    len_data = len(data)
    while sent != len_data:
        sent += client.send(data[sent:], 0)

s = udt.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
s.bind(("127.0.0.1", 5555))
s.listen(10)
i = 0
clients = {}
epoll = udt.epoll()


for x in xrange(0, threads):
    child, host = s.accept()
    child.setsockopt(0, udt.UDT_MAXBW, max_bandwidth)
    clients[child.fileno()] = child
    epoll.add_usock(child.fileno(), udt.UDT_EPOLL_IN)

while True:
    print 'wait..'
    sets = epoll.epoll_wait(-1)
    print sets
    poll = []
    for i in sets[0]:
        text = clients[i].recv(1024, 0)
        print text

        if text != "OK":
            p = Thread(target=test, args=(clients[i], text))
            p.start()
            poll.append(p)
        else:
            print text
            clients[i].send("OK", 0)
            clients[i].close()
            epoll.remove_usock(i)
            del clients[i]
    if not clients:
        epoll.release()
        break
for p in poll:
    p.join()

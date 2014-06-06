#!/usr/bin/env python
import udt
import socket
import time
import logging
import logging.config
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
from multiprocessing import Process


threads = 10
data_len = 1024 * 1024 * 10


def func():
    s = udt.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    s.connect(("localhost", 5555))
    asd = data_len
    s.send(str(asd), 0)
    t1 = time.time()
    while asd != 0:
        asd -= len(s.recv(asd, 0))
    log.info(time.time() - t1)
    s.send("OK", 0)
    log.info(s.recv(2, 0))
    s.close()

th_list = []
for x in xrange(0, threads):
    p = Process(target=func)
    p.start()
    th_list.append(p)
for p in th_list:
    p.join()

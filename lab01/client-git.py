# coding: utf-8

from socket import *
import json
from datetime import datetime
import selectors
import sys
import fcntl
import os

sel = selectors.DefaultSelector()                   # create a selector

def startConn():
    conn = socket(AF_INET, SOCK_STREAM)             # create an INET, STREAMing socket
    conn.connect(('localhost', 1234))               # connect to server (block until accepted)
    conn.setblocking(False)                         # ESSENTIAL -> configure socket to non-blocking mode
    sel.register(conn, selectors.EVENT_READ, read)
    return conn

def read(conn, stdin, mask):
    msg = conn.recv(1024).decode('utf-8')
    print(msg)

def write(conn, stdin, mask):
    msg=stdin.read()
    json_msg = json.dumps({"Timestamp": datetime.now().timestamp(),"Name":"Vasco Ramos","Message":msg.strip()})
    conn.send(json_msg.encode('utf-8'))             # send some data

def main():
    orig_fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL)
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)
    sel.register(sys.stdin, selectors.EVENT_READ, write)
    clientSocket = startConn()
    while True:
        sys.stdout.write('Type something and hit enter\n>')
        sys.stdout.flush()
        events = sel.select()
        for key, mask in events:
            key.data(clientSocket, key.fileobj, mask)
    sel.unregister(sys.stdin)                       # do I have to also unregister conn ??


if __name__ == '__main__':
main()
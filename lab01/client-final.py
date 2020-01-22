from socket import socket, AF_INET, SOCK_STREAM

import logging
import json
import selectors

from datetime import datetime

import sys
import fcntl
import os

logging.basicConfig(level = logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("CLIENT")
logger.setLevel(logging.INFO)


def read(socket,stdin,mask,sel):
    msg = socket.recv(1024).decode('UTF-8')
    data = json.loads(msg)['DATA']
    timestamp = json.loads(msg)['TIMESTAMP']
    logger.info("%s",data)

def write(socket,stdin,mask,sel):
    msg = stdin.read()
    
    data = json.dumps({"TIMESTAMP": datetime.now().timestamp(),"DATA":msg.strip()})
    socket.send(data.encode('UTF-8'))

def main():
    clientSocket = socket(AF_INET,SOCK_STREAM)
    clientSocket.connect(('localhost',2000))
    clientSocket.setblocking(False)

    orig_fl = fcntl.fcntl(sys.stdin, fcntl.F_GETFL) #https://stackoverflow.com/questions/21791621/taking-input-from-sys-stdin-non-blocking
    fcntl.fcntl(sys.stdin, fcntl.F_SETFL, orig_fl | os.O_NONBLOCK)

    sel = selectors.DefaultSelector() #Create selector
    sel.register(clientSocket,selectors.EVENT_READ,read) #IF key.fileobj = clientSocket, go to read
    sel.register(sys.stdin,selectors.EVENT_READ,write) #IF key.fileobj = sys.stdin, go to write

    while 1:  
        sys.stdout.write('>> ')
        sys.stdout.flush()

        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(clientSocket,key.fileobj, mask,sel)
            
    sel.unregister(sys.stdin)
    sel.unregister(clientSocket)
    clientSocket.close()

if __name__ == '__main__':
    main()
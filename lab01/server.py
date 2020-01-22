# coding: utf-8

from socket import *
import json
import selectors
import queue
import threading

sel = selectors.DefaultSelector()                   # create a selector
clientsDB = {}                                      # clients' data base
msgQ = queue.Queue()

# This function gets a message from the queue, decodes it and resends it
def work():
    while True:
        conn, data = msgQ.get()

        print('echoing', repr(data), 'to', conn)
        # Hope it won't block
        json_msg = json.loads(data.decode('utf-8'))
        
        if json_msg["Message"]=="exit":
            clientsDB.pop(conn.getpeername()[1])
            print(clientsDB)

        for port,connection in clientsDB.items():
            connection.send((str(json_msg["Timestamp"]) + " | from: " + str(conn.getpeername()[1] ) + " --> " + json_msg["Message"] + "*").encode('utf-8'))
    
# This function simply reads the message received and puts it in a queue
def read(conn, mask):
    data = conn.recv(1024)                          # Should be ready
    if data:
        msgQ.put((conn,data))
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

def dispatch():
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask) 
        

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)     # create an INET, STREAMing socket
    serverSocket.bind(('localhost', 1241))          # bind the socket to a public host, and a well-known port
    serverSocket.listen(5)                          # become a server socket    
    
    #Create and start the dispatcher thread 
    dispatcher = threading.Thread(target=dispatch) #Create new dispatcher thread
    dispatcher.start()

    #Create and start the 2 worker threads
    workers1 = threading.Thread(target=work)
    workers1.start()

    workers2 = threading.Thread(target=work)
    workers2.start()

    while True:
        clientSocket, addr = serverSocket.accept()  # Accept new client
        print('accepted', clientSocket, 'from', addr)

        ip, port = addr
        clientsDB[port] = clientSocket

        clientSocket.setblocking(False)
        sel.register(clientSocket, selectors.EVENT_READ, read)  # Register new client                                

    clientSocket.close()                            # close the connection

if __name__ == '__main__':
    main()
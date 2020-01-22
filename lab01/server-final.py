from socket import socket, AF_INET, SOCK_STREAM

import logging
import json
import queue
import threading
import selectors

msgQ = queue.Queue()
activeClients = {}

logging.basicConfig(level = logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ECHO_SERVER")
logger.setLevel(logging.DEBUG)

#This function gets a message from the queue, decodes it and resends it
def work():
    while True:
        socket,encodedData = msgQ.get()
        data = json.loads(encodedData.decode('UTF-8'))['DATA']
        timestamp = json.loads(encodedData.decode('UTF-8'))['TIMESTAMP']
        response = json.dumps({"TIMESTAMP": timestamp,"DATA":data.strip()})
        
        logger.info("Echoing %s to %s",response,socket)
        #socket.send(response.encode('UTF-8')) #Send the json through the socket where the message came from

        for port,connection in activeClients.items():
            #response = str("TIMESTAMP: " + timestamp + " " + port + " - " + data)
            connection.send(response.encode('UTF-8'))


#This function simply reads the message received and puts it in a queue
def read(socket,mask,sel):
    data = socket.recv(1024)
    logger.info("Received Message from %s",socket)

    if data: #If the data received is valid
        msgQ.put((socket,data)) #Put it in the queue
    else:
        logger.info('Closing %s',socket) #Terminate that socket
        sel.unregister(socket)
        socket.close()

def dispatch(sel):
    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data #Tell the selector which function to call
            callback(key.fileobj,mask,sel) #Call the function

def main():
    sel = selectors.DefaultSelector() #Create selector

    serverSocket = socket(AF_INET, SOCK_STREAM) #Open sockets
    serverSocket.bind(('localhost',2000))
    serverSocket.listen(5)

    #Create and start the dispatcher thread 
    dispatcher = threading.Thread(target=dispatch,args=(sel,)) #Create new dispatcher thread
    dispatcher.start()

    #Create and start the 2 worker threads
    workers1 = threading.Thread(target=work)
    workers1.start()

    workers2 = threading.Thread(target=work)
    workers2.start()

    #Register new client(s)
    while True:
        clientSocket, address = serverSocket.accept() #Accept new client
        clientSocket.setblocking(False)
        logger.info('Accepted from %s', address)

        ip, port = address
        activeClients[port] = clientSocket
        
        sel.register(clientSocket,selectors.EVENT_READ,read) #Register new client

    clientSocket.close()

if __name__ == '__main__':
    main()
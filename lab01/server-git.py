# coding: utf-8

from socket import *
import json
import selectors

sel = selectors.DefaultSelector()                   # create a selector
clientsDB = {}                                      # clients' data base
# away_messages=[]
# state_add=0

def accept(sock, mask):
    conn, addr = sock.accept()                      # Should be ready
    print('accepted', conn, 'from', addr)
    # print("\n" + str(addr) + "\n")

    ip, port = addr
    clientsDB[port] = conn

    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)
    # if len(away_messages)!=0:
    #     state_add=0
    #     for b in away_messages:
    #         conn.send(b)
    #     away_messages.clear()

def read(conn, mask):
    data = conn.recv(1024)                          # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        # Hope it won't block
        json_msg = json.loads(data.decode('utf-8'))

        if json_msg["Message"]=="exit":
            clientsDB.pop(conn.getpeername()[1])
            print(clientsDB)

        for port,connection in clientsDB.items():
            connection.send((str(json_msg["Timestamp"]) + " | " + json_msg["Name"] + " --> " + json_msg["Message"] + "*").encode('utf-8'))

    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)     # create an INET, STREAMing socket
    serverSocket.bind(('localhost', 1233))          # bind the socket to a public host, and a well-known port
    serverSocket.listen(5)                          # become a server socket
    serverSocket.setblocking(False)                 # ESSENTIAL -> configure socket to non-blocking mode
    sel.register(serverSocket, selectors.EVENT_READ, accept)

    while True:
        events = sel.select()
        for key, mask in events:
            key.data(key.fileobj, mask)                                     

    clientSocket.close()                            # close the connection

if __name__ == '__main__':
main()
import socket
from _thread import *
serversocket = socket.socket()
host = "127.0.0.1"
port = 1233
ThreadCount = 0

try:
    serversocket.bind((host, port))
except socket.error as e:
    print(str(e))
print("Waiting for a Connection..")
serversocket.listen(5)

def client_thread(connection):
    connection.send(str.encode("Welcome to the Servern"))
    while True:
        data = connection.recv(2048)
        reply = "Server Says: " + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()

while True:
    client, address = serversocket.accept()
    print("Connected to: " + address[0] + ":" + str(address[1]))
    start_new_thread(client_thread, (client,))
    ThreadCount += 1
    print("Thread Number: " + str(ThreadCount))
serversocket.close()
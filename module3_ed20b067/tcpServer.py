import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1',12345))
server_socket.listen(5)

while True:
    print("Waiting for connection...")
    client_socket, address = server_socket.accept() #introduces a new socket object to send and receive data on the connection, and a tuple holding the address of the client (host, port)
    print("Connection from: " + str(address))
    while True:
        data = client_socket.recv(1024)
        if not data or data.decode('utf-8') == 'END':
            break
        print("from connected user: " + data.decode('utf-8'))
        try:
            client_socket.send(bytes("Hello from server", 'utf-8'))
        except:
            print("Error sending data")
    client_socket.close()
server_socket.close() 

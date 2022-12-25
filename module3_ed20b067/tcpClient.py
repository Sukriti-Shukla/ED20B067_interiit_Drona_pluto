import socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1',12345))
payload = "Hello from client"

try:
    while True:
        client_socket.send(payload.encode('utf-8'))
        data = client_socket.recv(1024) #1024 is the buffer size
        print(str(data))
        more=input("More data? (y/n): ")
        if more.lower() == 'y':
            payload = input("Enter data: ")
        else:
            break
except KeyboardInterrupt:
    print("Closing socket")
client_socket.close()


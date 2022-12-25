# import socket

# # Create a UDP socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# # Bind the socket to the port
# server_address = ('0.0.0.0', 12345)
# print('starting up on ' + str(server_address))
# sock.bind(server_address)

# while True:
#     print('waiting to receive message')
#     try:
#         data, address = sock.recvfrom(4096)
#         print('received data from ' + str(address))
#         print(str(data))
#         message = b'Hello from the server'
#         sock.sendto(message, address)
#     except socket.timeout:
#         continue

    
import socket

localIP   = "127.0.0.1"
localPort = 12345
bufferSize = 1024

msgFromServer = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)


# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)


# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

print("UDP server up and listening")

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)

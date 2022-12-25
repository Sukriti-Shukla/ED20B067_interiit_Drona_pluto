import socket
import sys
#
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#first argument is address family, second is socket type
except socket.error as err:
    print("socket creation failed with error %s" %(err))
    sys.exit()
print("socket successfully created")

target_host = input("Enter the host to connect to: ")
target_port = input("Enter the port to connect to: ")
try:
    sock.connect((target_host, int(target_port)))
    print("socket connected to %s on port %s" %(target_host, target_port))
    sock.shutdown(2)
except socket.error as err:
    print("socket connection failed with error %s" %(err))
    sys.exit()


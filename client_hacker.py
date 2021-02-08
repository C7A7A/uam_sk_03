#!/usr/bin/env python3

from helper_methods_communication import *
from helper_methods_client import *
import socket

# HOST = 'grasieci.adiantek.ovh'
PORT = 5006
HOST = '150.254.79.171'

# HOST = 'localhost'
# PORT = 54321

client_socket = socket.socket()

try:
    client_socket.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

response = receive(client_socket)
print(response)
send(client_socket, 'LOGIN 452648\n')

x = 1

run = True
while run:
    try:
        data = receive(client_socket)
        print(data)
        sleep(5)
    except socket.time as e:
        print(e)

client_socket.close()

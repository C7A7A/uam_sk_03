#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 12345
client_socket = socket.socket()

print('Waiting for connection')
try:
    client_socket.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

response = client_socket.recv(1024)
while True:
    data = input('Siema, ja fan')
    client_socket.send(str.encode(data))
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

client_socket.close()
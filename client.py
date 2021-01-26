#!/usr/bin/env python3

import socket

HOST = '127.0.0.1'
PORT = 54321
client_socket = socket.socket()

try:
    client_socket.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

response = client_socket.recv(1024)
print(response.decode('utf-8'))
login = input('LOGIN ')
client_socket.send(str.encode(login))

while True:
    response = client_socket.recv(1024)
    print(response.decode('utf-8'))

client_socket.close()

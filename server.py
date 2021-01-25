#!/usr/bin/env python3

import socket
import os
from _thread import *


def threaded_client(connection):
    connection.send(str.encode('Welcome to the server\n'))
    while True:
        data = connection.recv(2048)
        reply = 'Server says: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
    connection.close()


HOST = '127.0.0.1'
PORT = 12345
thread_count = 0
server_socket = socket.socket()

try:
    server_socket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

print('Waiting for connection...')
server_socket.listen(4)

while True:
    client, address = server_socket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (client, ))
    thread_count += 1
    print('Thread number: ' + str(thread_count))

server_socket.close()



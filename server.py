#!/usr/bin/env python3

import socket
import os
from _thread import *


PLAYERS = 0


def is_login_incorrect(login):
    if not login:
        return True
    if ' ' in login:
        return True
    return False


def threaded_client(connection, player_num):
    connection.send(str.encode('CONNECT'))
    data = connection.recv(2048)
    login = data.decode('utf-8')
    if is_login_incorrect(login):
        connection.send(str.encode('Error: invalid login'))
        connection.close()
        return

    global PLAYERS
    PLAYERS += 1
    # print('Active players: ' + str(PLAYERS))

    if PLAYERS == 2:
        connection.send(str.encode('START'))


HOST = '127.0.0.1'
PORT = 54321
player_number = 0
server_socket = socket.socket()

try:
    server_socket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

server_socket.listen(4)

while True:
    client, address = server_socket.accept()
    player_number += 1
    start_new_thread(threaded_client, (client, player_number))

server_socket.close()

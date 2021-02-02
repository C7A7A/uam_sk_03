#!/usr/bin/env python3

from helper_methods_communication import *
from helper_methods_client import *
from Board import Board
import socket

HOST = '127.0.0.1'
PORT = 54321
client_socket = socket.socket()

try:
    client_socket.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

response = receive(client_socket)
print(response)
send(client_socket, 'LOGIN 452648')

available_choices = parse(receive(client_socket))
client_board = Board(200, 200)

run = True
while run:
    print('Available choices: ', available_choices)
    try:
        data = receive(client_socket)
        message = parse(data)
        if message == 'YOUR CHOICE':
            print('CHOOSE ' + str(available_choices[0]))
            send(client_socket, 'CHOOSE ' + str(available_choices[0]))
        elif message == 'PLAYER CHOICE':
            domino_taken = handle_player_choice(data)
            print('Remove: ', domino_taken)
            available_choices.remove(str(domino_taken))
        elif message == 'ROUND':
            available_choices = handle_round_choice(data)
        elif message == 'YOUR MOVE':
            print('MOVE 1 0 0')
            send(client_socket, 'MOVE 1 0 0')
        elif message == 'PLAYER MOVE':
            print('PLAYER MOVE')
        elif message == 'STOP':
            run = False
    except socket.error as e:
        print(e)

client_socket.close()

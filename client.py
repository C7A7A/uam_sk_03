#!/usr/bin/env python3

from helper_methods_communication import *
from helper_methods_client import *
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

available_choices = []
x = 1

run = True
while run:
    print('Available choices: ', available_choices)
    try:
        data = receive(client_socket)
        message = parse(data)
        if message == 'OK':
            print(message)
        elif message == 'ERROR':
            print(message)
        elif message == 'YOUR CHOICE':
            print('CHOOSE ' + str(available_choices[0]))
            send(client_socket, 'CHOOSE ' + str(available_choices[0]))
        elif message == 'PLAYER CHOICE':
            domino_taken = handle_player_choice(data)
            print('Remove: ', domino_taken)
            available_choices.remove(str(domino_taken))
        elif message == 'ROUND':
            available_choices = handle_round_choice(data)
        elif message == 'YOUR MOVE':
            print('MOVE ' + str(x) + ' 0 0')
            send(client_socket, 'MOVE ' + str(x) + ' 0 0')
            x += 2
        elif message == 'PLAYER MOVE':
            print(message)
        elif message == 'START':
            available_choices = handle_start(data)
        elif message == 'GAME OVER RESULTS':
            run = False
        elif message == 'UNKNOWN':
            print(message)
    except socket.error as e:
        print(e)

client_socket.close()

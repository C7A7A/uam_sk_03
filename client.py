#!/usr/bin/env python3

from helper_methods_communication import *
from helper_methods_client import *
from time import sleep
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

run = True
while run:
    print('Available choices: ', available_choices)
    try:
        sleep(1)
        data = receive(client_socket)
        message = parse(data)
        if message == 'YOUR CHOICE':
            print('CHOOSE ' + str(available_choices[0]))
            send(client_socket, 'CHOOSE ' + str(available_choices[0]))
        elif message == 'PLAYER CHOICE':
            domino_taken = handle_player_choice(data)
            available_choices.remove(str(domino_taken))
        elif message == 'ROUND':
            available_choices = handle_round_choice(data)
        elif message == 'STOP':
            run = False
    except socket.error as e:
        print(e)

client_socket.close()

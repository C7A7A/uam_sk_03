#!/usr/bin/env python3

from helper_methods_communication import *
from helper_methods_client import *
import socket

# HOST = 'grasieci.adiantek.ovh'
# PORT = 5006
# HOST = '150.254.79.172'

HOST = 'localhost'
PORT = 54321

client_socket = socket.socket()

try:
    client_socket.connect((HOST, PORT))
except socket.error as e:
    print(str(e))

response = receive(client_socket)
print(response)
send(client_socket, 'LOGIN 452648\n')

available_choices = []
x = 1

run = True
while run:
    # print('Available choices: ', available_choices)
    try:
        data = receive(client_socket)
        parsed_data = data.splitlines()
        # print(parsed_data)

        for message in range(len(parsed_data)):
            parsed_data[message] = parsed_data[message].split(' ')
        print(parsed_data)

        for message in range(len(parsed_data)):
            if parsed_data[message][0] == 'OK':
                continue
            elif parsed_data[message][0] == 'ROUND':
                available_choices = handle_round_choice(parsed_data[message])
            elif parsed_data[message][0] == 'START':
                available_choices = handle_start(parsed_data[message])
            elif parsed_data[message][0] == 'YOUR' and parsed_data[message][1] == 'CHOICE':
                # print('CHOOSE ' + str(available_choices[0]))
                send(client_socket, 'CHOOSE ' + str(available_choices[0]) + '\n')
                # send(client_socket, 'CHOOSE ' + '-1' + '\n')
            elif parsed_data[message][0] == 'PLAYER' and parsed_data[message][1] == 'CHOICE':
                domino_taken = handle_player_choice(parsed_data[message])
                # print('Remove: ', domino_taken)
                available_choices.remove(str(domino_taken))
            elif parsed_data[message][0] == 'YOUR' and parsed_data[message][1] == 'MOVE':
                print('MOVE ' + str(x) + ' 0 0')
                # send(client_socket, 'MOVE ' + 'ssijmikutasakurewko\n')
                send(client_socket, 'MOVE ' + str(x) + ' 0 0\n')
                x += 2
            elif parsed_data[message][0] == 'PLAYER' and parsed_data[message][1] == 'MOVE':
                continue
            elif parsed_data[message][0] == 'ERROR':
                continue
            else:
                run = False
    except socket.time as e:
        print(e)

client_socket.close()

#!/usr/bin/env python3

from helper_methods_communication import *
from helper_methods_server import *
from dominoes_list import *
import socket
from Board import Board

HOST = '127.0.0.1'
PORT = 54321

players_order = [1, 2]
players_order = shuffle_players(players_order)
dominoes_list = create_and_shuffle_dominoes_list()
available_dominoes = []
dominoes_choices = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

server_socket.listen(2)


def message_start(conn, player_num):
    start_data = 'START ' + str(player_num) + get_players_order_string(players_order) + \
                 get_dominoes_order_string(available_dominoes)
    print(start_data)
    send(conn, start_data)


def message_choice(conn):
    print('YOUR CHOICE')
    send(conn, 'YOUR CHOICE')
    choice = receive(conn)
    print(choice)
    choice = choice.replace('CHOOSE ', '')
    return int(choice)


def message_choice_player(player_num, choice, connections):
    for counter in range(len(connections)):
        if player_num != (counter + 1):
            send(connections[counter], 'PLAYER CHOICE ' + str(player_num) + ' ' + str(choice))


def message_round(conn, dominoes):
    string = ''
    for domino_number in range(len(dominoes)):
        string += ' '
        string += str(dominoes[domino_number])
    print('ROUND' + string)
    send(conn, 'ROUND' + string)


def message_move(conn):
    print('YOUR MOVE')
    send(conn, 'YOUR MOVE')
    move = receive(conn)
    print(move)
    move = move.replace('MOVE ', '')
    move = move.split(' ')
    print(move)
    return move


def message_move_player(player_num, move, connections):
    for counter in range(len(connections)):
        if player_num != (counter + 1):
            send(connections[counter], 'PLAYER MOVE ' + str(player_num) + ' ' + str(move[0]) + ' ' + str(move[1]) + ' '
                 + str(move[2]))


def message_stop(conn):
    send(conn, 'STOP')


connection_list = [get_connection_and_login(server_socket), get_connection_and_login(server_socket)]
player_boards = []

players_number = len(connection_list)
available_dominoes = get_available_dominoes(dominoes_list, 0, players_number)

for player in range(len(connection_list)):
    player_boards.append(Board(200, 200))

for player in range(len(connection_list)):
    message_start(connection_list[player], player + 1)

run = True
while run:
    try:
        for player in range(len(connection_list)):
            if players_order[player] == 1:
                choice = message_choice(connection_list[0])
                dominoes_choices.append([1, choice])
                message_choice_player(1, choice, connection_list)
            elif players_order[player] == 2:
                choice = message_choice(connection_list[1])
                dominoes_choices.append([2, choice])
                message_choice_player(2, choice, connection_list)

        print('Dominoes choices: ', dominoes_choices)
        sorted_dominoes_choices = sorted(dominoes_choices, key=lambda x: x[1])
        print('Sorted dominoes choices: ', sorted_dominoes_choices)
        for player in range(len(sorted_dominoes_choices)):
            players_order[player] = sorted_dominoes_choices[player][0]
        print('Players order: ', players_order)
        available_dominoes = get_available_dominoes(dominoes_list, players_number, players_number)
        print('Available dominoes: ', available_dominoes)

        for player in range(len(connection_list)):
            message_round(connection_list[player], available_dominoes)

        for player in range(len(connection_list)):
            if players_order[player] == 1:
                move = message_move(connection_list[0])
                # obsłuż jego planszę
                message_move_player(1, move, connection_list)
            elif players_order[player] == 2:
                move = message_move(connection_list[1])
                # obsłuż jego planszę
                message_move_player(2, move, connection_list)

        run = False
    except socket.error as e:
        print(e)

# def new_player(connection, player_num):
#     send(connection, 'CONNECT')
#     login = receive(connection)
#     if is_login_incorrect(login):
#         connection.close()
#         return
#
#     global players
#     players += 1
#
#     while True:
#         if players == 2:
#             global available_dominoes
#             available_dominoes = get_available_dominoes(dominoes_list, players)
#
#             start_data = 'START ' + str(player_num) + get_players_order_string(players_order) + \
#                          get_dominoes_order_string(available_dominoes)
#             send(connection, start_data)
#
#             global turn
#
#             while True:
#                 if player_num == players_order[turn]:
#                     send(connection, 'YOUR CHOICE')
#
#                     global response
#                     response = receive(connection)
#
#                     connection.close()
#                     print(response)
#                     if turn < players:
#                         turn += 1
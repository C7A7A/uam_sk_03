#!/usr/bin/env python3

from helper_methods_server import *
from dominoes_list import *
import socket
from Board import Board

HOST = '127.0.0.1'
PORT = 54321

players_order = [1, 2, 3, 4]
players_order = shuffle_players(players_order)
dominoes_list = create_and_shuffle_dominoes_list()
available_dominoes = []
dominoes_choices = {}
domino_counter = 0

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

server_socket.listen(4)


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
    print('PLAYER CHOICE ' + str(player_num) + ' ' + str(choice))
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
    move = move.replace('MOVE ', '')
    move = move.split(' ')
    print(move)
    return move


def message_move_player(player_num, move, connections):
    print('PLAYER MOVE ' + str(player_num) + ' ' + str(move[0]) + ' ' + str(move[1]) + ' ' + str(move[2]))
    for counter in range(len(connections)):
        if player_num != (counter + 1):
            send(connections[counter], 'PLAYER MOVE ' + str(player_num) + ' ' + str(move[0]) + ' ' + str(move[1]) + ' '
                 + str(move[2]))


connection_list = [
    get_connection_and_login(server_socket),
    get_connection_and_login(server_socket),
    get_connection_and_login(server_socket),
    get_connection_and_login(server_socket)
]

player_board = []

players_number = len(connection_list)
available_dominoes = get_available_dominoes(dominoes_list, 0, players_number)

for player in range(players_number):
    player_board.append(Board(49, 49))

for player in range(players_number):
    message_start(connection_list[player], player + 1)

for game_round in range(12):
    try:
        for player in range(players_number):
            if players_order[player] == 1:
                choice = message_choice(connection_list[0])
                dominoes_choices[1] = choice
                message_choice_player(1, choice, connection_list)
            elif players_order[player] == 2:
                choice = message_choice(connection_list[1])
                dominoes_choices[2] = choice
                message_choice_player(2, choice, connection_list)
            elif players_order[player] == 3:
                choice = message_choice(connection_list[2])
                dominoes_choices[3] = choice
                message_choice_player(3, choice, connection_list)
            elif players_order[player] == 4:
                choice = message_choice(connection_list[3])
                dominoes_choices[4] = choice
                message_choice_player(4, choice, connection_list)

        print('Dominoes choices: ', dominoes_choices)
        sorted_dominoes_choices = sorted(dominoes_choices.items(), key=lambda x: x[1])
        print('Sorted dominoes choices: ', sorted_dominoes_choices)
        for player in range(len(sorted_dominoes_choices)):
            players_order[player] = sorted_dominoes_choices[player][0]
        print('Players order: ', players_order)
        domino_counter += players_number
        available_dominoes = get_available_dominoes(dominoes_list, domino_counter, players_number)
        print('Available dominoes: ', available_dominoes)

        for player in range(players_number):
            message_round(connection_list[player], available_dominoes)

        for player in range(players_number):
            if players_order[player] == 1:
                move = message_move(connection_list[0])
                domino_choice = dominoes_choices[1]
                domino = next((x for x in dominoes_list if x.number == domino_choice), None)
                player_board[0].update_board(int(move[0]), int(move[1]), int(move[2]), domino)
                message_move_player(1, move, connection_list)
            elif players_order[player] == 2:
                move = message_move(connection_list[1])
                domino_choice = dominoes_choices[2]
                domino = next((x for x in dominoes_list if x.number == domino_choice), None)
                player_board[1].update_board(int(move[0]), int(move[1]), int(move[2]), domino)
                message_move_player(2, move, connection_list)
            elif players_order[player] == 3:
                move = message_move(connection_list[2])
                domino_choice = dominoes_choices[3]
                domino = next((x for x in dominoes_list if x.number == domino_choice), None)
                player_board[2].update_board(int(move[0]), int(move[1]), int(move[2]), domino)
                message_move_player(3, move, connection_list)
            elif players_order[player] == 4:
                move = message_move(connection_list[3])
                domino_choice = dominoes_choices[3]
                domino = next((x for x in dominoes_list if x.number == domino_choice), None)
                player_board[3].update_board(int(move[0]), int(move[1]), int(move[2]), domino)
                message_move_player(4, move, connection_list)

    except socket.error as e:
        print(e)

for player in range(players_number):
    send(connection_list[player], 'GAME OVER RESULTS')
    connection_list[player].close()

for player in range(players_number):
    for i in range(len(player_board[player].board)):
        for j in range(len(player_board[player].board[i])):
            print(player_board[player].board[i][j], end=' ')
        print()
    print()

server_socket.close()

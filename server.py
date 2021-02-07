#!/usr/bin/env python3

from helper_methods_server import *
from dominoes_list import *
import socket
from Board import Board
from Area import Area

HOST = '150.254.79.126'
# HOST = 'localhost'
PORT = 54321

text_file = open('output.txt', 'w')

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((HOST, PORT))
except socket.error as e:
    print(str(e))

server_socket.listen(1)


def get_connection_and_login(sock, player_num):
    conn, address = sock.accept()
    send(conn, 'CONNECT\n')
    login = receive(conn)
    login = login.rstrip()
    print(login)
    if validate_login(login):
        send(conn, 'OK\n')
    else:
        send(conn, 'ERROR\n')
        players_errors[player_num - 1] += 1
        if players_errors[player_num - 1] > 100:
            close_connection(player_num - 1)
            return
        get_connection_and_login(sock, player_num)
    players_login[player_num] = login.replace('LOGIN ', '')
    return conn


def message_start(conn, player_num):
    start_data = 'START ' + str(player_num) + get_players_order_string(players_order) + \
                 get_dominoes_order_string(available_dominoes) + '\n'
    text_file.write(start_data)
    print(start_data)
    send(conn, start_data)


def message_choice(conn, player_num):
    print('YOUR CHOICE')
    text_file.write('YOUR CHOICE\n')

    send(conn, 'YOUR CHOICE\n')

    choice = receive(conn)
    text_file.write(choice)
    choice = choice.rstrip()
    print(choice)

    if validate_choice(choice):
        send(conn, 'OK\n')
    else:
        send(conn, 'ERROR\n')
        players_errors[player_num - 1] += 1
        # if players_errors[player_num - 1] > 100:
            # print('errors.count > 100')
        # message_choice(conn, player_num)
    choice = choice.replace('CHOOSE ', '')
    return int(choice)


def message_choice_player(player_num, choice, connections):
    print('PLAYER CHOICE ' + str(player_num) + ' ' + str(choice))
    for counter in range(len(connections)):
        if player_num != (counter + 1):
            text_file.write('PLAYER CHOICE ' + str(player_num) + ' ' + str(choice) + '\n')
            send(connections[counter], 'PLAYER CHOICE ' + str(player_num) + ' ' + str(choice) + '\n')


def handle_choice(player_num):
    choice = message_choice(connection_list[player_num - 1], player_num)
    if choice == -1:
        return
    dominoes_choices[player_num] = choice
    message_choice_player(player_num, choice, connection_list)


def message_round(conn, dominoes):
    string = ''
    for domino_number in range(len(dominoes)):
        string += ' '
        string += str(dominoes[domino_number])
    string += '\n'
    text_file.write('ROUND' + string)
    print('ROUND' + string)
    send(conn, 'ROUND' + string)


def message_move(conn, player_num):
    text_file.write('YOUR MOVE\n')
    print('YOUR MOVE')
    send(conn, 'YOUR MOVE\n')
    move = receive(conn)
    text_file.write(move)
    move = move.rstrip()
    if validate_move(move):
        send(conn, 'OK\n')
    else:
        send(conn, 'ERROR\n')
        players_errors[player_num - 1] += 1
        if players_errors[player_num - 1] > 100:
            close_connection(player_num - 1)
            return
        message_move(conn, player_num)
    move = move.replace('MOVE ', '')
    move = move.split(' ')
    print(move)
    return move


def message_move_player(player_num, move, connections):
    print('PLAYER MOVE ' + str(player_num) + ' ' + str(move[0]) + ' ' + str(move[1]) + ' ' + str(move[2]))
    for counter in range(len(connections)):
        if player_num != (counter + 1):
            text_file.write('PLAYER MOVE ' + str(player_num) + ' ' + str(move[0]) + ' ' + str(move[1]) + ' ' + str(move[2]) + '\n')
            send(connections[counter], 'PLAYER MOVE ' + str(player_num) + ' ' + str(move[0]) + ' ' + str(move[1]) + ' ' + str(move[2]) + '\n')


def handle_move(player_num):
    move = message_move(connection_list[player_num - 1], player_num)
    domino_choice = dominoes_choices[player_num]
    domino = next((x for x in dominoes_list if x.number == domino_choice), None)
    player_boards[player_num - 1].update_board(int(move[0]), int(move[1]), int(move[2]), domino)
    message_move_player(player_num, move, connection_list)


def count_points(board):
    forest, grass, sand, bog, water, mine = [], [], [], [], [], []
    points = 0
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] != 0 and board[x][y] != 'CA':
                domino_type, crowns = parse_domino(board[x][y])
                if domino_type == 'f':
                    sort_dominoes_by_area_type(forest, x, y, crowns)
                elif domino_type == 'g':
                    sort_dominoes_by_area_type(grass, x, y, crowns)
                elif domino_type == 's':
                    sort_dominoes_by_area_type(sand, x, y, crowns)
                elif domino_type == 'b':
                    sort_dominoes_by_area_type(bog, x, y, crowns)
                elif domino_type == 'w':
                    sort_dominoes_by_area_type(water, x, y, crowns)
                elif domino_type == 'm':
                    sort_dominoes_by_area_type(mine, x, y, crowns)

    print('forest')
    for i in range(len(forest)):
        print(forest[i].coordinates)
    print('grass')
    for i in range(len(grass)):
        print(grass[i].coordinates)
    print('sand')
    for i in range(len(sand)):
        print(sand[i].coordinates)
    print('bog')
    for i in range(len(bog)):
        print(bog[i].coordinates)
    print('water')
    for i in range(len(water)):
        print(water[i].coordinates)
    print('mine')
    for i in range(len(mine)):
        print(mine[i].coordinates)
    points += count_area_type(forest)
    points += count_area_type(grass)
    points += count_area_type(sand)
    points += count_area_type(bog)
    points += count_area_type(water)
    points += count_area_type(mine)
    # print(points)
    return points


def parse_domino(domino):
    parsed_domino = list(domino)
    return parsed_domino[0], int(parsed_domino[1])


def sort_dominoes_by_area_type(area_type, x, y, crowns):
    if len(area_type) == 0:
        new_area = Area()
        new_area.add_domino(x, y, crowns)
        area_type.append(new_area)
    else:
        stop = False
        for area in range(len(area_type)):
            for domino in range(len(area_type[area].coordinates)):
                coordinates = area_type[area].coordinates[domino]
                # SPRAWDŹ LEWO -> GÓRĘ
                if (x - 1) == coordinates[0] and y == coordinates[1]:
                    area_type[area].add_domino(x, y, crowns)
                    if x == coordinates[0] and (y - 1) == coordinates[1]:
                        area_type[area].add_domino(x, (y - 1), crowns)
                    stop = True
                    break
                # SPRAWDŹ GÓRĘ
                if x == coordinates[0] and (y - 1) == coordinates[1]:
                    area_type[area].add_domino(x, y, crowns)
                    stop = True
                    break
            if stop:
                break
        # NIE JEST POŁĄCZONY, DODAJ NOWE SKUPISKO
        if not stop:
            new_area = Area()
            new_area.add_domino(x, y, crowns)
            area_type.append(new_area)


def count_area_type(area_type):
    pts = 0
    for area in range(len(area_type)):
        pts += (area_type[area].crowns * area_type[area].dominoes)
    # print('points: ', pts)
    return pts


def close_connection(player_num):
    connection_list[player_num].close()
    global players_number


dominoes_list = create_and_shuffle_dominoes_list()
dominoes_choices = {}
domino_counter = 0
players_login = {}

connection_list = [
    get_connection_and_login(server_socket, 1)
    # get_connection_and_login(server_socket, 2),
    # get_connection_and_login(server_socket, 3),
    # get_connection_and_login(server_socket, 4)
]

player_boards = []
players_number = len(connection_list)
players_order = [*range(1, players_number + 1)]
players_order = shuffle_players(players_order)
players_errors = [0] * players_number

available_dominoes = get_available_dominoes(dominoes_list, 0)

for player in range(players_number):
    player_boards.append(Board(53, 53))

for player in range(players_number):
    message_start(connection_list[player], player + 1)

for game_round in range(12):
    try:
        for player in range(players_number):
            if players_order[player] == 1:
                handle_choice(1)
            elif players_order[player] == 2:
                handle_choice(2)
            elif players_order[player] == 3:
                handle_choice(3)
            elif players_order[player] == 4:
                handle_choice(4)

        # print('Dominoes choices: ', dominoes_choices)
        sorted_dominoes_choices = sorted(dominoes_choices.items(), key=lambda x: x[1])
        # print('Sorted dominoes choices: ', sorted_dominoes_choices)
        for player in range(len(sorted_dominoes_choices)):
            players_order[player] = sorted_dominoes_choices[player][0]
        # print('Players order: ', players_order)
        domino_counter += 4
        available_dominoes = get_available_dominoes(dominoes_list, domino_counter)
        print('Available dominoes: ', available_dominoes)

        for player in range(players_number):
            message_round(connection_list[player], available_dominoes)

        for player in range(players_number):
            if players_order[player] == 1:
                handle_move(1)
            elif players_order[player] == 2:
                handle_move(2)
            elif players_order[player] == 3:
                handle_move(3)
            elif players_order[player] == 4:
                handle_move(4)

    except socket.timeout as e:
        print(e)

for player in range(players_number):
    for i in range(len(player_boards[player].board)):
        for j in range(len(player_boards[player].board[i])):
            print(player_boards[player].board[i][j], end=' ')
        print()
    print()

points = {}

for player in range(players_number):
    points[player + 1] = (count_points(player_boards[player].board))

points = sorted(points.items(), key=lambda x: x[1], reverse=True)

string = ''
for player in range(players_number):
    string += str(players_login[points[player][0]]) + ' ' + str(points[player][1]) + ' '
string = string[:-1]
string += '\n'

for player in range(players_number):
    text_file.write('GAME OVER RESULTS ' + string)
    send(connection_list[player], 'GAME OVER RESULTS ' + string)
    connection_list[player].close()

print('GAME OVER RESULTS ' + string)

server_socket.close()

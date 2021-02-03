import random
from helper_methods_communication import *


def get_connection_and_login(server_socket):
    conn, address = server_socket.accept()
    send(conn, 'CONNECT')
    login = receive(conn)
    print(login)
    if is_login_incorrect(login):
        conn.close()
        return
    return conn


def is_login_incorrect(login):
    login = login.replace('LOGIN ', '')
    if not login:
        return True
    if ' ' in login:
        return True
    return False


def shuffle_players(players):
    random.shuffle(players)
    return players


def get_players_order_string(players_order):
    string = ''
    for player in range(len(players_order)):
        string += ' '
        string += str(players_order[player])
    return string


def get_available_dominoes(dominoes_list, start, players):
    available_dominoes = []
    for counter in range(start, start + players):
        if counter < len(dominoes_list):
            available_dominoes.append(dominoes_list[counter].number)
    available_dominoes.sort()
    return available_dominoes


def get_dominoes_order_string(available_dominoes):
    string = ''
    for counter in range(len(available_dominoes)):
        string += ' '
        string += str(available_dominoes[counter])
    return string

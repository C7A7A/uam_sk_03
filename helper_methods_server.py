import random
from helper_methods_communication import *


def validate_login(login):
    if 'LOGIN ' not in login:
        return False
    login = login.replace('LOGIN ', '')
    if not login:
        return False
    if ' ' in login:
        return False
    return True


def validate_choice(choice, raw_choice):
    if len(raw_choice) > 250:
        return False
    if 'CHOOSE ' not in choice:
        return False
    choice = choice.replace('CHOOSE ', '')
    if not choice:
        return False
    parsed_choice = choice.split(' ')
    print(parsed_choice)
    print(parsed_choice[0])
    if len(parsed_choice) == 1:
        if try_parse_to_int(parsed_choice[0]):
            if int(parsed_choice[0]) in range(1, 49):
                return True
    return False


def validate_move(move, raw_move):
    if len(raw_move) > 250:
        return False
    if 'MOVE ' not in move:
        return False
    move = move.replace('MOVE ', '')
    if not move:
        return False
    parsed_move = move.split(' ')
    if len(parsed_move) == 3:
        if try_parse_to_int(parsed_move[0]) or try_parse_to_int(parsed_move[1]) or try_parse_to_int(parsed_move[2]):
            if int(parsed_move[0]) not in range(-100, 100) or int(parsed_move[1]) not in range(-100, 100):
                return False
            if int(parsed_move[2]) not in [0, 90, 180, 270]:
                return False
            return True
    return False


def try_parse_to_int(data):
    try:
        int(data)
        return True
    except ValueError:
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


def get_available_dominoes(dominoes_list, start):
    available_dominoes = []
    for counter in range(start, start + 4):
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

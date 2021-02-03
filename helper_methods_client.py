def parse(data):
    parsed_string = data.split(' ')
    print(parsed_string)
    if parsed_string[0] == 'START':
        return parse_start(parsed_string)
    elif parsed_string[0] == 'YOUR' and parsed_string[1] == 'CHOICE':
        return 'YOUR CHOICE'
    elif parsed_string[0] == 'PLAYER' and parsed_string[1] == 'CHOICE':
        return 'PLAYER CHOICE'
    elif parsed_string[0] == 'ROUND':
        return 'ROUND'
    elif parsed_string[0] == 'YOUR' and parsed_string[1] == 'MOVE':
        return 'YOUR MOVE'
    elif parsed_string[0] == 'PLAYER' and parsed_string[1] == 'MOVE':
        return 'PLAYER MOVE'
    elif parsed_string[0] == 'GAME':
        return 'GAME OVER RESULTS'
    else:
        return 'UNKNOWN'


def parse_start(parsed):
    del(parsed[0:4])
    # print(parsed)
    return parsed


def handle_player_choice(data):
    parsed_string = data.split(' ')
    print(parsed_string[3])
    return parsed_string[3]


def handle_round_choice(data):
    parsed_string = data.split(' ')
    del(parsed_string[0])
    available_dominoes = []
    for i in range(len(parsed_string)):
        available_dominoes.append(parsed_string[i])
    print(available_dominoes)
    return available_dominoes

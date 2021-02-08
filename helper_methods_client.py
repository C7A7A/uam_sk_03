def parse(data):
    parsed_string = data.split(' ')
    parsed_string[-1] = parsed_string[-1].strip()
    print(parsed_string)
    if parsed_string[0] == 'OK':
        return 'OK'
    elif parsed_string[0] == 'ERROR':
        return 'ERROR'
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
    elif parsed_string[0] == 'START':
        return 'START'
    elif parsed_string[0] == 'GAME':
        return 'GAME OVER RESULTS'
    else:
        return 'UNKNOWN'


def handle_start(data):
    del(data[0:6])
    return data


def handle_player_choice(data):
    return data[3]


def handle_round_choice(data):
    del(data[0])
    available_dominoes = []
    for i in range(len(data)):
        available_dominoes.append(data[i])
    # print(available_dominoes)
    return available_dominoes

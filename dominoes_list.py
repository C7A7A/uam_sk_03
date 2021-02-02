from Domino import Domino
import random


def create_and_shuffle_dominoes_list():
    dominoes_list = [
        Domino(1, 's', 's'), Domino(2, 's', 's'), Domino(3, 'f', 'f'),
        Domino(4, 'f', 'f'), Domino(5, 'f', 'f'), Domino(6, 'f', 'f'),
        Domino(7, 'w', 'w'),  Domino(8, 'w', 'w'),  Domino(9, 'w', 'w'),
        Domino(10, 'g', 'g'), Domino(11, 'g', 'g'), Domino(12, 'b', 'b'),
        Domino(13, 's', 'f'), Domino(14, 's', 'w'), Domino(15, 's', 'g'),
        Domino(16, 's', 'b'), Domino(17, 'f', 'w'), Domino(18, 'f', 'g'),
        Domino(19, 's', 'f', 1), Domino(20, 's', 'w', 1), Domino(21, 's', 'g', 1),
        Domino(22, 's', 'b', 1), Domino(23, 's', 'm', 1), Domino(24, 'f', 's', 1),
        Domino(25, 'f', 's', 1), Domino(26, 'f', 's', 1), Domino(27, 'f', 's', 1),
        Domino(28, 'f', 'w', 1), Domino(29, 'f', 'g', 1), Domino(30, 'w', 's', 1),
        Domino(31, 'w', 's', 1), Domino(32, 'w', 'f', 1), Domino(33, 'w', 'f', 1),
        Domino(34, 'w', 'f', 1), Domino(35, 'w', 'f', 1), Domino(36, 's', 'g', 0, 1),
        Domino(37, 'w', 'g', 0, 1), Domino(38, 's', 'b', 0, 1), Domino(39, 'g', 'b', 0, 1),
        Domino(40, 'm', 's', 1, 0), Domino(41, 's', 'g', 0, 2), Domino(42, 'w', 'g', 0, 2),
        Domino(43, 's', 'b', 0, 2), Domino(44, 'g', 'b', 0, 2), Domino(45, 'm', 's', 2, 0),
        Domino(46, 'b', 'm', 0, 2), Domino(47, 'b', 'm', 0, 2), Domino(48, 's', 'm', 0, 3)
    ]

    random.shuffle(dominoes_list)
    return dominoes_list

class Board:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.board = [[0 for size_x in range(size_x)] for size_y in range(size_y)]
        self.board[24][24] = 'CA'

    def update_board(self, x, y, orientation, domino):
        x = x + 24
        y = y + 24
        print('x: ', x, 'y: ', y)
        if x < 0 or x > 49 or y < 0 or y > 49:
            return False
        if self.board[x][y] == 0:
            if self.board[x + 1][y] != 0 or self.board[x - 1][y] != 0 or self.board[x][y + 1] != 0 or self.board[x][y - 1] != 0:
                if orientation == 0:
                    if self.board[x + 1][y] == 0:
                        self.board[x][y] = domino.type_1 + str(domino.crowns_1)
                        self.board[x + 1][y] = domino.type_2 + str(domino.crowns_2)
                        return True
                elif orientation == 90:
                    if self.board[x][y + 1] == 0:
                        self.board[x][y] = domino.type_1 + str(domino.crowns_1)
                        self.board[x][y + 1] = domino.type_2 + str(domino.crowns_2)
                        return True
                elif orientation == 180:
                    if self.board[x - 1][y] == 0:
                        self.board[x][y] = domino.type_1 + str(domino.crowns_1)
                        self.board[x - 1][y] = domino.type_2 + str(domino.crowns_2)
                        return True
                elif orientation == 270:
                    if self.board[x][y - 1] == 0:
                        self.board[x][y] = domino.type_1 + str(domino.crowns_1)
                        self.board[x][y - 1] = domino.type_2 + str(domino.crowns_2)
                        return True
        return False

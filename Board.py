class Board:
    def __init__(self, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.board = [[0 for x in range(size_x)] for y in range(size_y)]
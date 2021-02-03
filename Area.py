class Area:
    def __init__(self):
        self.dominoes = 0
        self.crowns = 1
        self.coordinates = []

    def add_domino(self, x, y, crowns=0):
        self.dominoes += 1
        self.crowns += crowns
        self.coordinates.append([x, y])

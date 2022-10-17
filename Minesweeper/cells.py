# for both under and cover cells?
class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.revealed = False
        self.highlighted = False
        self.flagged = False
        self.mine = False
        self.indicator = 0
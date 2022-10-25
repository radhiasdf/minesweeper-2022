# for both under and cover cells?
import random
import pygame.transform
from Minesweeper.constants import COVER_IMG, LOWER_CELL_IMG
degrees = [0, 90, 180, 270]
class Cell:
    def __init__(self, row, col, sqsize):
        self.row = row
        self.col = col
        self.revealed = False
        self.highlighted = False
        self.flagged = False
        self.mine = False
        self.indicator = 0
        self.random_rotation = degrees[random.randint(0, len(degrees)-1)]
        self.lower_img = pygame.transform.rotate(
            pygame.transform.scale(LOWER_CELL_IMG, (sqsize, sqsize)),
            self.random_rotation).convert()
        self.cover_img = pygame.transform.rotate(
            pygame.transform.scale(COVER_IMG, (sqsize, sqsize)),
            self.random_rotation).convert()
        # random texture rotation to make it more seamless
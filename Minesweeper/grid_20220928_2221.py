import pygame
from .constants import *
import random
mine = 'X'
squaresize = MINSQSIZE

class Grid:
    def __init__(self):
        self.grid = []

    def draw_checkerboard(self, win, setcols, setrows, colour1, colour2):
        win.fill(colour1)

        # draws a checkerboard pattern
        for row in range(setrows):
            # the '%' tells if the row is odd or even to shift the alternating pattern so it doesn't become stripes
            for col in range(row % 2, setcols, 2):
                pygame.draw.rect(win, colour2, (col*squaresize, row*squaresize, squaresize, squaresize))

class Underfield(Grid):
    def __init__(self, num_cols, num_rows, minerarity, win):
        field = [[0 for _ in range(num_cols)] for _ in range(num_rows)]

        # adding mines
        num_mines = int(round((num_rows * num_cols) / minerarity))
        minecount = num_mines

        while minecount > 0:
            row, col = random.randint(0, num_rows - 1), random.randint(0, num_cols - 1)
            print(row, col)
            if field[row][col] != mine:
                field[row][col] = mine
                minecount -= 1

        # adding number indicators for every non-bomb cell, with checking if out of range
        for row in range(num_rows):
            for col in range(num_cols):
                count = 0
                if field[row][col] != mine:
                    if col > 0:
                        if field[row][col - 1] == mine: count += 1  # left
                    if col < num_cols - 1:
                        if field[row][col + 1] == mine: count += 1  # right
                    if row > 0:
                        if field[row - 1][col] == mine: count += 1  # up
                    if row < num_rows - 1:
                        if field[row + 1][col] == mine: count += 1  # down

                    if row > 0 and col > 0:
                        if field[row - 1][col - 1] == mine: count += 1  # top left
                    if row > 0 and col < num_cols - 1:
                        if field[row - 1][col + 1] == mine: count += 1  # top right
                    if row < num_rows - 1 and col > 0:
                        if field[row + 1][col - 1] == mine: count += 1  # bottom left
                    if row < num_rows - 1 and col < num_cols - 1:
                        if field[row + 1][col + 1] == mine: count += 1  # bottom right
                    field[row][col] = count

        self.field = field



    def draw_data(self, win):
        for row in range(10): # replace this
            for col in range(10):
                if self.field[row][col] == mine:
                    win.blit(MINE_IMG, (col*squaresize, row*squaresize))

class Coverfield(Grid):
    pass

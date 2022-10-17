import pygame
from .constants import *
import random
from queue import Queue

mine = -1
sqsize = MINSQSIZE

class Grid:
    def __init__(self, win, setcols, setrows):
        self.win = win
        self.cols = setcols
        self.rows = setrows
        self.field = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def draw_checkerboard(self, colour1, colour2):
        self.win.fill(colour1)

        # draws a checkerboard pattern
        for row in range(self.rows):
            # the '%' tells if the row is odd or even to shift the alternating pattern so it doesn't become stripes
            for col in range(row % 2, self.cols, 2):
                pygame.draw.rect(self.win, colour2, (col*sqsize, row*sqsize, sqsize, sqsize))

    def get_surrounding(self, row, col):  # surrounding cells' coordinates,to generalise finding mines and uncovering
        surrounding = []
        if col > 0:
            surrounding.append([row, col - 1])  # left
        if col < self.cols - 1:
            surrounding.append([row, col + 1])  # right
        if row > 0:
            surrounding.append([row - 1, col])  # up
        if row < self.rows - 1:
            surrounding.append([row + 1, col])  # down

        if row > 0 and col > 0:
            surrounding.append([row - 1, col - 1])  # top left
        if row > 0 and col < self.cols - 1:
            surrounding.append([row - 1, col + 1])  # top right
        if row < self.rows - 1 and col > 0:
            surrounding.append([row + 1, col - 1])  # bottom left
        if row < self.rows - 1 and col < self.cols - 1:
            surrounding.append([row + 1, col + 1])  # bottom right
        return surrounding


class Underfield(Grid):
    def __init__(self, win, setcols, setrows, minerarity):
        super().__init__(win, setcols, setrows)

        # adding mines
        num_mines = int(round((self.rows * self.cols) / minerarity))
        minecount = num_mines
        while minecount > 0:
            row, col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            print(row, col)
            if self.field[row][col] != mine:
                self.field[row][col] = mine
                minecount -= 1

        # adding number indicators for every non-bomb cell, with checking if out of range
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col] == mine:
                    continue
                indicator = 0
                surrounding = Grid.get_surrounding(self, row, col)
                print(surrounding)
                for r, c in surrounding:
                    if self.field[r][c] == mine:
                        indicator += 1
                self.field[row][col] = indicator

    def draw_data(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col] == mine:
                    self.win.blit(MINE_IMG, (col*sqsize + (sqsize-MINE_IMG.get_width())/2, row*sqsize
                                             + (sqsize-MINE_IMG.get_height())/2))
                elif self.field[row][col] != 0:
                    text = NUM_FONT.render(str(self.field[row][col]), True, NUM_COLOURS[self.field[row][col]])
                    self.win.blit(text, (col*sqsize + (sqsize-text.get_width())/2, row*sqsize
                                             + (sqsize-text.get_height())/2))


class Coverfield(Grid):
    def draw_checkerboard(self, colour1, colour2):  # specific to cover field...
        # draws a checkerboard pattern
        for row in range(self.rows):
            for col in range((row+1) % 2, self.cols, 2):
                if self.field[row][col] == 0:
                    pygame.draw.rect(self.win, colour1, (col * sqsize, row * sqsize, sqsize, sqsize))
            for col in range(row % 2, self.cols, 2):
                if self.field[row][col] == 0:
                    pygame.draw.rect(self.win, colour2, (col * sqsize, row * sqsize, sqsize, sqsize))

    def reveal(self,mousepos, underfield):
        col = int(mousepos[0]/sqsize)
        row = int(mousepos[1]/sqsize)
        self.field[row][col] = 1

        # revealing all 0s and numbers adjacent
        q = Queue()
        q.put((row, col))
        found = []
        while not q.empty():
            current = q.get()
            surrounding = Grid.get_surrounding(self, *current)

            for r, c in surrounding:
                if (r, c) in found:
                    continue
                if underfield.field[r][c] >= 0:
                    found.append((r, c))
                    if underfield.field[r][c] == 0:
                        q.put((r, c))
                    self.field[r][c] = 1

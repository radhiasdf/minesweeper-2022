import pygame
from .constants import *


class Underfield:
    def __init__(self):
        self.underfield = []

    def draw_squares(self, win, setcols, setrows, winwidth, winheight):
        win.fill(LIGHTERGREEN)

        if setcols > 30 or setrows > 30:
            squaresize = FIXEDSQSIZE
        else:
            squaresize = 600/setcols

        # draws a checkerboard pattern
        for row in range(setrows):
            # the '%' tells if the row is odd or even to shift the alternating patten so it doesnt become stripes
            for col in range(row % 2, setcols, 2):
                pygame.draw.rect(win, DARKERGREEN, (col*squaresize, row*squaresize, squaresize, squaresize))

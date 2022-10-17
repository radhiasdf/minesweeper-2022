import random
import time
import pygame
from itertools import chain
from Minesweeper.grid import *
from Minesweeper.constants import *


num_rows, num_cols = 16, 30
num_mines = 9  # There's a mine in every [] squares, 5 is hard, 8 is easy

"""# 'small' grid so square size depends on window height
if DEFAULTWINHEIGHT / num_rows > MINSQSIZE or DEFAULTWINHEIGHT / num_cols > MINSQSIZE:  
    width, height = DEFAULTWINHEIGHT*(num_cols/num_rows), DEFAULTWINHEIGHT
    sqsize = DEFAULTWINHEIGHT / num_rows
else:  # 'big' grid so window depends on grid size with minimum square size"""

width, height = MINSQSIZE * num_cols, MINSQSIZE * num_rows + SIDEBAR_HEIGHT

print(width, height)

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("minesweeper WITH BIRCH SIGNS!!!")

FPS = 60
global start_time
global clicks


def main():
    global start_time
    global clicks
    start_time = 0

    run = True
    clock = pygame.time.Clock()
    coverfield = Coverfield(win, num_cols, num_rows)
    underfield = Underfield(win, num_cols, num_rows)
    clicks = 0
    state = "playing"

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mousepos = pygame.mouse.get_pos()
                row, col = int(mousepos[1] / sqsize), int(mousepos[0] / sqsize)  # assigning xy position to grid
                mousepressed = pygame.mouse.get_pressed()
                print(mousepressed)
                if mousepressed[0]:  # left click
                    if clicks == 0:
                        underfield.generate_data(row, col, num_mines)
                        start_time = time.time()
                    coverfield.reveal(row, col, underfield)
                    clicks += 1

                else:
                    coverfield.editflag(row, col)

        update(underfield, coverfield)


def update(underfield, coverfield):
    if clicks > 0: stopwatch = int(time.time() - start_time)
    else: stopwatch = 0

    win.fill(BG_COLOUR)
    underfield.draw_checkerboard(LIGHTBROWN, DARKBROWN)
    underfield.draw_data()
    coverfield.draw_board(LIGHTGREEN, DARKGREEN)

    text = WIN_FONT.render(str(stopwatch), True, "white")
    win.blit(text, (10, height - SIDEBAR_HEIGHT + (SIDEBAR_HEIGHT-text.get_height())/2))

    if sum(coverfield.field, []).count(concealed) + sum(coverfield.field, []).count(
            flagged) == underfield.num_mines:
        finish()

    pygame.display.update()


def finish():
    text = WIN_FONT.render(WIN_MESSAGE, True, "white")
    win.blit(text, (width-text.get_width()-10, height - SIDEBAR_HEIGHT + (SIDEBAR_HEIGHT-text.get_height())/2))


def lose():
    print('nnnnnnnnnoooooooooooo')

while True:
    main()

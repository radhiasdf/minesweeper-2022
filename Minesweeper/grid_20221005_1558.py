import pygame
from .constants import *
import random
from queue import Queue

mine = -1


# probably make a class for the cells?
class Grid:
    sqsize = MINSQSIZE

    def __init__(self, win, setcols, setrows):
        self.win = win
        self.cols = setcols
        self.rows = setrows
        self.field = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.data_generated = False

    def draw_checkerboard_cell(self, row, col, colour1, colour2, image):
        if (row + col) % 2 == 0:  # draws a checkerboard pattern
            colour = colour2
        else:
            colour = colour1
        pygame.draw.rect(self.win, colour, (col * self.sqsize, row * self.sqsize, self.sqsize, self.sqsize))
        self.win.blit(image, (col * self.sqsize, row * self.sqsize), special_flags=pygame.BLEND_MULT)

    # gets surrounding cells' coordinates,to generalise finding mines and uncovering
    def get_surrounding(self, row, col):
        surrounding = []
        if col > 0:
            surrounding.append((row, col - 1))  # left
        if col < self.cols - 1:
            surrounding.append((row, col + 1))  # right
        if row > 0:
            surrounding.append((row - 1, col))  # up
        if row < self.rows - 1:
            surrounding.append((row + 1, col))  # down

        if row > 0 and col > 0:
            surrounding.append((row - 1, col - 1))  # top left
        if row > 0 and col < self.cols - 1:
            surrounding.append((row - 1, col + 1))  # top right
        if row < self.rows - 1 and col > 0:
            surrounding.append((row + 1, col - 1))  # bottom left
        if row < self.rows - 1 and col < self.cols - 1:
            surrounding.append((row + 1, col + 1))  # bottom right
        return surrounding


class Underfield(Grid):
    def __init__(self, win, setcols, setrows, coverfield):
        super().__init__(win, setcols, setrows)
        self.num_mines = None
        self.coverfield = coverfield  # necessary for only drawing numbers in open coverfield cells

    # generates mines and number indicators
    def generate_data(self, mrow, mcol, num_mines):
        # if the user flags at the beginning then clicks on the flag then its not revealed
        if self.coverfield.field[mrow][mcol] == self.coverfield.flagged or self.data_generated:
            return
        # adding mines
        invalidplaces = Grid.get_surrounding(self, mrow, mcol)
        print(f'starting click coords: ({mrow},{mcol})')
        print(f'invalidplaces: {invalidplaces}')
        invalidplaces.append((mrow, mcol))

        self.num_mines = num_mines
        minecount = num_mines
        while minecount > 0:
            row, col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.field[row][col] != mine and (
                    row, col) not in invalidplaces:  # at the 1st click mines shouldnt be spawned near the clicked cell
                self.field[row][col] = mine
                minecount -= 1
                if (row, col) in invalidplaces: print(f'{minecount} i disobeyed')

        # adding number indicators for every non-bomb cell, with checking if out of range
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col] == mine:
                    continue
                indicator = 0
                surrounding = Grid.get_surrounding(self, row, col)
                for r, c in surrounding:
                    if self.field[r][c] == mine:
                        indicator += 1
                self.field[row][col] = indicator
        for row in self.field: print(row)
        self.data_generated = True

    def draw_iterate_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.draw_checkerboard_cell(row, col, "white", "gray96", LOWER_CELL_IMG)
                # so highlighting doesn't reveal the numbers
                if self.coverfield.field[row][col] == self.coverfield.revealed:
                    self.draw_number(row, col)

    def draw_number(self, row, col):
        if self.field[row][col] > 0:
            text = NUM_FONT.render(str(self.field[row][col]), True, NUM_COLOURS[
                self.field[row][col]])  # to make them centered; there should be a simpler way
            self.win.blit(text, (col * self.sqsize + (self.sqsize - text.get_width()) / 2,
                                 row * self.sqsize + (self.sqsize - text.get_height()) / 2))

    def draw_mines(self):  # has own iteration for now
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col] == mine:
                    self.win.blit(MINE_IMG, (col * self.sqsize + (self.sqsize - MINE_IMG.get_width()) / 2,
                                             row * self.sqsize + (self.sqsize - MINE_IMG.get_height()) / 2))
        print("mines drawn")


class Coverfield(Grid):
    def __init__(self, win, setcols, setrows):
        super().__init__(win, setcols, setrows)
        self.concealed = 0
        self.revealed = 1
        self.flagged = 2
        self.highlighted = 3

    def highlight_update(self, mouse_row, mouse_col, mousepressed):
        # checking every cell, if theyre either concealed or highlighted and mouse is pressed, highlight, otherwise conceal back
        # less bugs would prb occur if the cells were a class
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col] in (self.concealed, self.highlighted):
                    if 0 <= mouse_row < self.rows and 0 <= mouse_col < self.cols:  # if mouse in grid
                        if (mouse_row, mouse_col) == (row, col) and mousepressed[0]:
                            self.field[row][col] = self.highlighted
                            if mousepressed[2]:
                                self.highlight_chord(row, col)

                        else:
                            self.field[row][col] = self.concealed
                    else:
                        self.field[row][col] = self.concealed

    def highlight_chord(self, row, col):
        for r, c in self.get_surrounding(row, col):
            if self.field[r][c] == self.concealed:
                self.field[r][c] = self.highlighted

    # revealing the cover field from the cell clicked
    def reveal(self, row, col, underfield):
        if self.field[row][col] == self.flagged:  # click has no effect on flagged cell
            return
        self.field[row][col] = self.revealed
        if underfield.field[row][col] > 0:
            return  # if the revealed cell is a number, just reveal that one
        elif underfield.field[row][col] == mine:
            self.reveal_cells_over_mines(underfield)
            return "gameover"

        # pathfinding and revealing all 0s and numbers adjacent
        q = Queue()
        q.put((row, col))
        found = set()
        while not q.empty():
            current = q.get()
            surrounding = Grid.get_surrounding(self, *current)

            for r, c in surrounding:
                if (r, c) in found:
                    continue
                if self.field[r][c] == self.flagged:
                    continue
                if underfield.field[r][c] >= 0:
                    found.add((r, c))
                    if underfield.field[r][c] == 0:
                        q.put((r, c))
                    self.field[r][c] = self.revealed

    def reveal_cells_over_mines(self, underfield):  # edits data
        for row in range(self.rows):
            for col in range(self.cols):
                if underfield.field[row][col] == mine:
                    self.field[row][col] = self.revealed

    def editflag(self, row, col):  # edits data
        if self.field[row][col] == self.revealed:
            return
        if self.field[row][col] == self.flagged:
            self.field[row][col] = self.concealed
        else:
            self.field[row][col] = self.flagged

    def draw_shadows(self):  # very simple shadows...
        for row in range(self.rows):  # not included in iteration collective draw thing bc the whole field needs to be shadowed first rather than per cell, so the next cell's shadow isn't blitted after the previous cell's cover
            for col in range(self.cols):
                if self.field[row][col] not in (self.revealed, self.highlighted):
                    pygame.draw.rect(self.win, SHADOW_COLOUR, (col * self.sqsize + THREE_D_OFFSET_X,
                                                               row * self.sqsize + THREE_D_OFFSET_Y,
                                                               self.sqsize, self.sqsize))
        """for (xpos, ypos, width, height) in [(0, -1, self.win.get_width(), self.sqsize)]:
            pygame.draw.rect(self.win, SHADOW_COLOUR, (xpos * self.sqsize + THREE_D_OFFSET_X,
                                                   ypos * self.sqsize + THREE_D_OFFSET_Y,
                                                   width, height))"""

    def draw_iterate_cells(self):  # drawing unrevealed cells and flags
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col] not in (self.revealed, self.highlighted):
                    self.draw_checkerboard_cell(row, col, "darkolivegreen3", "darkolivegreen3", COVER_IMG)
                self.draw_data(row, col)

    def draw_data(self, row, col):
        # Draws flag for marked
        if self.field[row][col] == self.flagged:
            self.win.blit(SIGN_IMG, (col * self.sqsize + (self.sqsize - SIGN_IMG.get_width()) / 2,
                                     row * self.sqsize + (self.sqsize - SIGN_IMG.get_height()) / 2))

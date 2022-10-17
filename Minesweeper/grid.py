import pygame
from .cells import *
from .constants import *
import random
from queue import Queue

mine = -1


# probably make a class for the cells?
class Grid:
    sqsize = MINSQSIZE

    def __init__(self, win, setcols, setrows, game):
        self.game = game
        self.win = win
        self.cols = setcols
        self.rows = setrows
        self.field = [[Cell(row, col) for col in range(self.cols)] for row in range(self.rows)]
        self.num_mines = 0
        self.start_time = pygame.time.get_ticks()

        print(self.field)

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

    # generates mines and number indicators
    def generate_data(self, mrow, mcol, num_mines):
        # adding mines
        invalidplaces = Grid.get_surrounding(self, mrow, mcol)
        print(f'starting click coords: ({mrow},{mcol})')
        print(f'invalidplaces: {invalidplaces}')
        invalidplaces.append((mrow, mcol))

        self.num_mines = num_mines
        minecount = num_mines
        iterations = 0
        while minecount > 0:
            """positions = []
            for i in range(len(self.rows)):
                for j in range(len(self.cols)):
                    positions.append((i, j))
            row, col = positions.pop(random.randint(0, self.rows*self.cols))"""
            row, col = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            # at the 1st click mines shouldnt be spawned near the clicked cell

            if not self.field[row][col].mine:
                if num_mines <= self.rows * self.cols - 9:
                    if (row, col) not in invalidplaces:
                        self.field[row][col].mine = True
                        minecount -= 1
                elif num_mines <= self.rows * self.cols - 1:
                    if (row, col) not in invalidplaces:
                        self.field[row][col].mine = True
                        minecount -= 1
                    elif minecount <= num_mines - (self.rows*self.cols - 9) and (row, col) != (mrow, mcol):
                        self.field[row][col].mine = True
                        minecount -= 1
                else:
                    self.field[row][col].mine = True
                    minecount -= 1
            iterations += 1
        print(iterations)

        # adding number indicators for every non-bomb cell, with checking if out of range
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col].mine:
                    continue
                indicator = 0
                surrounding = Grid.get_surrounding(self, row, col)
                for r, c in surrounding:
                    if self.field[r][c].mine:
                        indicator += 1
                self.field[row][col].indicator = indicator

    def highlight_update2(self, mouse_row, mouse_col, mousepressed):
        # checking every cell; if theyre either concealed or highlighted and mouse is pressed then highlight, otherwise
        # conceal back
        to_be_highlighted = []
        for row in range(self.rows):
            for col in range(self.cols):
                if 0 <= mouse_row < self.rows and 0 <= mouse_col < self.cols:  # if mouse in grid
                    if (mouse_row, mouse_col) == (row, col) and mousepressed[0]:
                        self.field[row][col].highlighted = True
                        to_be_highlighted = [(row, col)]
                        # for highlighting chords
                        if mousepressed[2]:
                            for r, c in self.get_surrounding(row, col):
                                self.field[r][c].highlighted = True
                                to_be_highlighted.append((r, c))

                    elif (row, col) not in to_be_highlighted:
                        self.field[row][col].highlighted = False
                elif (row, col) not in to_be_highlighted:
                    self.field[row][col].highlighted = False

    # revealing the cover field from the cell clicked
    def reveal(self, row, col, underfield, mousepressed):
        if self.field[row][col].flagged or self.field[row][col].revealed:  # click has no effect on flagged cell
            return
        self.field[row][col].revealed = True
        if not pygame.mixer.get_busy():
            DIGSOUNDS[random.randint(0, len(DIGSOUNDS) - 1)].play()
        if underfield.field[row][col].indicator > 0:
            return  # if the revealed cell is a number, just reveal that one
        elif underfield.field[row][col].mine:
            return "gameover"

        # pathfinding and revealing all 0s and numbers adjacent
        q = Queue()
        q.put((row, col))
        found = set()
        while not q.empty():
            current = q.get()
            surrounding = Grid.get_surrounding(self, *current)

            for r, c in surrounding:
                if (r, c) in found:   # to prevent infinite loop revisiting cells
                    continue
                if self.field[r][c].flagged:
                    continue
                if underfield.field[r][c].indicator >= 0:
                    found.add((r, c))
                    if underfield.field[r][c].indicator == 0:
                        q.put((r, c))
                    self.field[r][c].revealed = True

    def reveal_cells_over_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col].mine:
                    self.field[row][col].revealed = True

    def editflag(self, row, col):
        if self.field[row][col].revealed:
            return
        if self.field[row][col].flagged:
            self.field[row][col].flagged = False
            self.game.counters.flag_count += 1
        else:
            self.field[row][col].flagged = True
            self.game.counters.flag_count -= 1
        FLAGSOUNDS[random.randint(0, len(FLAGSOUNDS)-1)].play()

    # draws the lower layer
    def under_draw_iterate_cells(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.draw_checkerboard_cell(row, col, "white", "gray96", LOWER_CELL_IMG)
                # so highlighting doesn't reveal the numbers
                if self.field[row][col].revealed:
                    self.draw_number(row, col)

    # draws every indicator number with their respective colours
    def draw_number(self, row, col):
        if self.field[row][col].indicator > 0:
            text = NUM_FONT.render(str(self.field[row][col].indicator), True, NUM_COLOURS[
                self.field[row][col].indicator])  # to make them centered; there should be a simpler way
            self.win.blit(text, (col * self.sqsize + (self.sqsize - text.get_width()) / 2,
                                 row * self.sqsize + (self.sqsize - text.get_height()) / 2))

    def draw_mines(self):  # has its own for loops for now
        for row in range(self.rows):
            for col in range(self.cols):
                if self.field[row][col].mine:
                    self.win.blit(MINE_IMG, (col * self.sqsize + (self.sqsize - MINE_IMG.get_width()) / 2,
                                             row * self.sqsize + (self.sqsize - MINE_IMG.get_height()) / 2))
        print("mines drawn")

    def draw_shadows(self):  # very simple shadows...
        def draw_shadow():
            pygame.draw.rect(self.win, SHADOW_COLOUR, (col * self.sqsize + THREE_D_OFFSET_X,
                                                       row * self.sqsize + THREE_D_OFFSET_Y,
                                                       self.sqsize, self.sqsize))
        # not included in collective draw for loops bc the whole field needs to be shadowed first rather than per
        # cell, so the next cell's shadow isn't blitted after the previous cell's cover
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.field[row][col].revealed and not self.field[row][col].highlighted:
                    draw_shadow()
                elif self.field[row][col].highlighted and self.field[row][col].flagged:
                    draw_shadow()

    def cover_draw_iterate_cells(self):  # drawing unrevealed cells and flags
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.field[row][col].revealed and not self.field[row][col].highlighted:  # so highlighed looks like revealed
                    self.draw_checkerboard_cell(row, col, "darkolivegreen3", "darkolivegreen3", COVER_IMG)
                elif self.field[row][col].highlighted and self.field[row][col].flagged:
                    self.draw_checkerboard_cell(row, col, "darkolivegreen3", "darkolivegreen3", COVER_IMG)
                self.draw_data(row, col)

    def draw_data(self, row, col):
        # Draws flag for marked
        if self.field[row][col].flagged:
            self.win.blit(SIGN_IMG, (col * self.sqsize + (self.sqsize - SIGN_IMG.get_width()) / 2,
                                     row * self.sqsize + (self.sqsize - SIGN_IMG.get_height()) / 2))

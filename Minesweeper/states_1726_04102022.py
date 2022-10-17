import time
from Minesweeper.constants import *
from Minesweeper.grid import *
from Minesweeper.gui import *
import pygame


class State:
    def __init__(self, game):
        self.game = game

    def update(self, events):
        pass

# pls ok now i want to make it so that it can press the face button and settings at any state...


class StartPlaying(State):
    def __init__(self, game):
        super().__init__(game)
        self.start_time = 0
        self.clicks = 0
        self.mousepressed = False
        self.start_time = 0
        self.coverfield = Coverfield(self.game.win, self.game.num_cols, self.game.num_rows)
        self.underfield = Underfield(self.game.win, self.game.num_cols, self.game.num_rows)
        self.emoticon = IDLE_FACE

    def update(self, events):
        # mouse-grid interaction
        self.mousepos = pygame.mouse.get_pos()
        row, col = int(self.mousepos[1] / self.coverfield.sqsize), int(self.mousepos[0] / self.coverfield.sqsize)  # assigning xy position to grid

        for e in events:
            if 0 <= row < self.game.num_rows and 0 <= col < self.game.num_cols:
                self.mousedown_in_grid(e, row, col)

        # rendering
        self.game.win.fill(BG_COLOUR)
        self.underfield.draw_checkerboard("white", "gray96")
        self.underfield.draw_data()
        self.coverfield.draw_board("darkolivegreen3", "darkolivegreen3")
        self.game.face_button.draw_face_button(self.emoticon)

        # stopwatch
        if self.clicks > 0:
            stopwatch = int(time.time() - self.start_time)
        else: stopwatch = 0
        text = SIDEBAR_FONT.render(str(stopwatch), True, "white")
        self.game.win.blit(text, (10, self.game.win_height - SIDEBAR_HEIGHT + (SIDEBAR_HEIGHT - text.get_height()) / 2))

        if sum(self.coverfield.field, []).count(self.coverfield.concealed) + sum(self.coverfield.field, []).count(
                self.coverfield.flagged) == self.underfield.num_mines:
            self.game.current_states.pop()
            self.game.current_states.append(WinYay(self.game))

    def mousedown_in_grid(self, e, row, col):
        if e.type == pygame.MOUSEBUTTONDOWN:
            self.mousepressed = pygame.mouse.get_pressed()
            print(self.mousepressed)
            if self.mousepressed[0]:
                self.coverfield.highlight(row, col, self.mousepressed)
            else:
                self.coverfield.editflag(row, col)
            self.emoticon = MOUSEDOWN_FACE

        if e.type == pygame.MOUSEBUTTONUP:
            if self.mousepressed[0]:  # left click
                if self.clicks == 0:
                    self.underfield.generate_data(row, col, self.game.num_mines)
                    self.start_time = time.time()
                if self.coverfield.reveal(row, col, self.underfield) == "gameover":
                    self.game.current_states.pop()
                    self.game.current_states.append(Lose(self.game))
                self.clicks += 1
            self.emoticon = IDLE_FACE


class WinYay(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, events):
        self.game.face_button.draw_face_button(WIN_FACE)


class Lose(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, events):
        self.game.face_button.draw_face_button(LOSE_FACE)


class Settings(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, event):
        pass
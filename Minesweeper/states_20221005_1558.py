import time
from Minesweeper.constants import *
from Minesweeper.grid import *
from Minesweeper.gui import *
import pygame


# what a chunk of redundancy ridden code idk

class State:
    def __init__(self, game):
        self.game = game

    def update(self, events):
        pass


# pls ok now i want to make it so that it can press the face button and settings at any state, but have those things in a state object


class StartPlaying(State):
    def __init__(self, game):
        super().__init__(game)
        self.clicks = 0
        self.start_time = 0
        # these grids can be accessed by more than one state bc there the game's attributes but the references become very long
        self.game.coverfield = Coverfield(self.game.win, self.game.num_cols, self.game.num_rows)
        self.game.underfield = Underfield(self.game.win, self.game.num_cols, self.game.num_rows, self.game.coverfield)
        self.emoticon = IDLE_FACE
        self.gameover = False
        self.stopwatch = 0
        self.mousepos = (0, 0)
        self.mousepressed = (False, False, False)
        self.time_started = False
        # specifically for storing which button would later be released
        self.mousepressed_at_mousedown = (False, False, False)

    def update(self, events):  # handles inputs given when playing and not at win or lose
        # mouse-grid position and pressed or not
        self.mousepos = pygame.mouse.get_pos()
        self.mousepressed = pygame.mouse.get_pressed()

        # assigning xy position to grid
        mouse_row = int(self.mousepos[1] / self.game.coverfield.sqsize)
        mouse_col = int(self.mousepos[0] / self.game.coverfield.sqsize)

        # highlighting cell(s) that are pressed but not mouse up
        self.game.coverfield.highlight_update(mouse_row, mouse_col, self.mousepressed)

        for e in events:
            # if mouse is in grid
            if 0 <= mouse_row < self.game.num_rows and 0 <= mouse_col < self.game.num_cols:
                # the instant the mouse is pressed down, not continuous
                if e.type == pygame.MOUSEBUTTONDOWN:
                    # again, specifically for storing which button would later be released
                    self.mousepressed_at_mousedown = self.mousepressed
                    print(f'mouse button down, {self.mousepressed_at_mousedown}')

                    if not self.mousepressed_at_mousedown[0]:
                        self.game.coverfield.editflag(mouse_row, mouse_col)

                # generates data if clicking the first time and reveals cells every click on a covered cell + check gameover
                if e.type == pygame.MOUSEBUTTONUP:
                    print(f'mouse button up, {self.mousepressed_at_mousedown}')
                    # left click # aha! self.mousepressed was constantly reseting every frame so field cant be revealed
                    if self.mousepressed_at_mousedown[0]:
                        # checking if its already generated is in underfield class (which is prb bad or should be changed)
                        self.game.underfield.generate_data(mouse_row, mouse_col, self.game.num_mines)
                        # starts stopwatch
                        if self.game.underfield.data_generated and not self.time_started:
                            self.start_time = time.time()
                            self.time_started = True
                        # calling method to reveal cells + losing
                        if self.game.coverfield.reveal(mouse_row, mouse_col, self.game.underfield) == "gameover":
                            self.game.current_states.pop()
                            self.game.current_states.append(Lose(self.game))
                            self.gameover = True
                        # winning
                        elif sum(self.game.coverfield.field, []).count(self.game.coverfield.concealed) \
                                + sum(self.game.coverfield.field, []).count(
                            self.game.coverfield.flagged) == self.game.underfield.num_mines:
                            self.game.current_states.pop()
                            self.game.current_states.append(WinYay(self.game))

                        self.clicks += 1

        # stopwatch
        if self.time_started:
            self.stopwatch = int(time.time() - self.start_time)
        else:
            self.stopwatch = 0

        if self.mousepressed[0]: self.emoticon = MOUSEDOWN_FACE
        else: self.emoticon = IDLE_FACE

        self.render()

    def render(self):
        # rendering
        self.game.win.fill(BG_COLOUR)
        self.game.underfield.draw_iterate_cells()
        if self.gameover:
            self.game.underfield.draw_mines()
        self.game.coverfield.draw_shadows()
        self.game.coverfield.draw_iterate_cells()
        self.game.face_button.draw_face_button(self.emoticon)

        text = SIDEBAR_FONT.render(str(self.stopwatch), True, "white")
        self.game.win.blit(text, (10, self.game.win_height - SIDEBAR_HEIGHT + (SIDEBAR_HEIGHT - text.get_height()) / 2))


class WinYay(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, events):
        self.game.face_button.draw_face_button(WIN_FACE)


class Lose(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, events):  # do animations or smt
        self.game.face_button.draw_face_button(LOSE_FACE)


class Settings(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, event):
        pass

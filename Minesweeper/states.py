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


class StartPlaying(State):
    def __init__(self, game):
        super().__init__(game)
        self.clicks = 0
        self.start_time = 0
        self.data_generated = False
        # this grid can be accessed by more than one state bc there the game's attributes but the references become very long
        self.game.field = Grid(self.game.win, self.game.num_cols, self.game.num_rows, self.game)
        self.emoticon = IDLE_FACE
        self.gameover = False
        self.game.counters = Counters(self.game)
        self.flag_count = self.game.num_mines

        self.mousepos = (0, 0)
        self.mousepressed = (False, False, False)
        # specifically for storing which button would later be released
        self.mpressed_at_mdown = (False, False, False)

    def update(self, events):  # handles inputs given when playing and not at win or lose
        # mouse-grid position and pressed or not
        self.mousepos = pygame.mouse.get_pos()
        self.mousepressed = pygame.mouse.get_pressed()
        to_be_highlighted = []

        # assigning xy position to grid
        m_row = int(self.mousepos[1] / self.game.field.sqsize)
        m_col = int(self.mousepos[0] / self.game.field.sqsize)

        # highlighting cell(s) that are pressed but not mouse up
        self.game.field.highlight_update2(m_row, m_col, self.mousepressed)

        # face expression update
        if 0 <= m_row < self.game.num_rows and 0 <= m_col < self.game.num_cols:
            if self.mousepressed[0]: self.emoticon = MOUSEDOWN_FACE
            else: self.emoticon = IDLE_FACE
        else: self.emoticon = IDLE_FACE

        for e in events:
            # if mouse is in grid
            if 0 <= m_row < self.game.num_rows and 0 <= m_col < self.game.num_cols:
                # the instant the mouse is pressed down, not continuous
                if e.type == pygame.MOUSEBUTTONDOWN:
                    # again, specifically for storing which button would later be released
                    self.mpressed_at_mdown = self.mousepressed
                    print(f'mouse button down, {self.mpressed_at_mdown}')

                    if not self.mpressed_at_mdown[0]:
                        self.game.field.editflag(m_row, m_col)

                # generates data if clicking the first time and reveals cells every click on a covered cell + check gameover
                if e.type == pygame.MOUSEBUTTONUP:
                    print(f'mouse button up, {self.mpressed_at_mdown}')
                    # aha! self.mousepressed was constantly resetting every frame so field cant be revealed

                    if self.mpressed_at_mdown[0] and not self.mpressed_at_mdown[2]:

                        if not self.game.field.field[m_row][m_col].flagged and not self.data_generated:
                            self.game.field.generate_data(m_row, m_col, self.game.num_mines)
                            self.data_generated = True
                            # starts stopwatch
                            self.game.counters.reset_stopwatch()
                        if self.game.field.reveal(m_row, m_col, self.game.field, self.mousepressed) == "gameover":
                            self.gameover = True
                        # calling method to reveal cells + losing
                        # chord clicks, checking if the indicator matches the number of flags put around so it reveals

                    if self.mpressed_at_mdown[0] and self.mpressed_at_mdown[2] and self.data_generated and self.game.field.field[m_row][m_col].revealed:
                        num_flagged = 0
                        surrounding = self.game.field.get_surrounding(m_row, m_col)
                        for r, c in surrounding:
                            if self.game.field.field[r][c].flagged:
                                num_flagged += 1
                        if num_flagged == self.game.field.field[m_row][m_col].indicator:
                            for r, c in surrounding:
                                if self.game.field.reveal(r, c, self.game.field, self.mousepressed) == "gameover":
                                    self.gameover = True
                            if self.game.field.reveal(m_row, m_col, self.game.field, self.mousepressed) == "gameover":
                                self.gameover = True

                    # losing
                    if self.gameover:
                        self.game.counters.stopwatch_paused = True
                        self.emoticon = LOSE_FACE
                        self.game.current_states.append(Lose(self.game))

                    # winning
                    else:
                        num_revealed = 0
                        for row in self.game.field.field:
                            num_revealed += [cell.revealed for cell in row].count(False)
                        if num_revealed == self.game.field.num_mines:
                            self.game.counters.stopwatch_paused = True
                            self.emoticon = WIN_FACE
                            self.game.current_states.append(WinYay(self.game))

                        self.clicks += 1

        self.render()

    def render(self):
        # rendering
        self.game.field.under_draw_iterate_cells()
        if self.gameover:
            self.game.field.draw_mines()
            self.game.field.reveal_cells_over_mines()
        self.game.field.draw_shadows()
        self.game.field.cover_draw_iterate_cells()
        self.game.face_button.update_n_draw(self.game.win_width / 2 - BUTTON_SPACING - BUTTON_IMGS[0].get_width(),
                                    (self.game.win_height - SIDEBAR_HEIGHT) + (SIDEBAR_HEIGHT / 2), ycentred=True, text=self.emoticon)

        self.game.counters.update_n_render()


class WinYay(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, events):
        # previous state is still rendered
        self.game.current_states[-2].render()


class Lose(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, events):  # do animations or smt
        self.game.current_states[-2].render()
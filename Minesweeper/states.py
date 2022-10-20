from Minesweeper.grid import *
from Minesweeper.gui import *
from Minesweeper.animations import *
import pygame


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
        self.game.field = Grid(self.game.win, self.game.num_cols, self.game.num_rows, self.game)
        self.field = self.game.field
        self.emoticon = IDLE_FACE
        self.gameover = False
        self.game.counters = Counters(self.game)
        self.flag_count = self.game.num_mines

        pygame.mixer.music.stop()

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
        self.game.m_row = int((self.mousepos[1] - self.field.ypos) / self.field.sqsize)
        self.game.m_col = int((self.mousepos[0] - self.field.xpos) / self.field.sqsize)
        m_row, m_col = self.game.m_row, self.game.m_col

        # highlighting cell(s) that are pressed but not mouse up
        self.field.highlight_update2(m_row, m_col, self.mousepressed)

        # face expression update
        if 0 <= m_row < self.game.num_rows and 0 <= m_col < self.game.num_cols:
            if self.mousepressed[0]: self.emoticon = MOUSEDOWN_FACE
            else: self.emoticon = IDLE_FACE
        else: self.emoticon = IDLE_FACE

        for e in events:
            # if mouse is in grid
            if 0 <= m_row < self.game.num_rows and 0 <= m_col < self.game.num_cols:
                # the data is of the instant the mouse is pressed down and doesnt continuously change
                if e.type == pygame.MOUSEBUTTONDOWN:
                    # again, specifically for storing which button would later be released
                    self.mpressed_at_mdown = self.mousepressed
                    print(f'mouse button down, {self.mpressed_at_mdown}')

                    if not self.mpressed_at_mdown[0]:
                        self.field.editflag(m_row, m_col)

                # generates data if clicking the first time and reveals cells every click on a covered cell + check gameover
                if e.type == pygame.MOUSEBUTTONUP:
                    print(f'mouse button up, {self.mpressed_at_mdown}')
                    # aha! self.mousepressed was constantly resetting every frame so field cant be revealed. the solution is storing which mousebuttons down only at the instant its pressed

                    if self.mpressed_at_mdown[0] and not self.mpressed_at_mdown[2]:

                        if not self.field.field[m_row][m_col].flagged and not self.data_generated:
                            self.field.generate_data(m_row, m_col, self.game.num_mines)
                            self.data_generated = True
                            # starts stopwatch
                            self.game.counters.reset_stopwatch()
                        if self.field.reveal(m_row, m_col) == "gameover":
                            self.gameover = True

                    # calling method to reveal cells + losing
                    # chord clicks, checking if the indicator matches the number of flags put around so it reveals
                    if self.mpressed_at_mdown[0] and self.mpressed_at_mdown[2] and self.data_generated and self.field.field[m_row][m_col].revealed:
                        num_flagged = 0
                        surrounding = self.field.get_surrounding(m_row, m_col)
                        for r, c in surrounding:
                            if self.field.field[r][c].flagged:
                                num_flagged += 1
                        if num_flagged == self.field.field[m_row][m_col].indicator:
                            for r, c in surrounding:
                                if self.field.reveal(r, c) == "gameover":
                                    self.gameover = True
                            if self.field.reveal(m_row, m_col) == "gameover":
                                self.gameover = True

                    # losing
                    if self.gameover:
                        self.game.counters.stopwatch_paused = True
                        self.emoticon = LOSE_FACE
                        self.game.current_states.append(Lose(self.game))

                    # winning
                    else:
                        num_revealed = 0
                        for row in self.field.field:
                            num_revealed += [cell.revealed for cell in row].count(False)
                        if num_revealed == self.field.num_mines:
                            self.game.counters.stopwatch_paused = True
                            self.emoticon = WIN_FACE
                            self.game.current_states.append(WinYay(self.game))

                        self.clicks += 1
                if e.type == pygame.MOUSEWHEEL:
                    if e.y == 0:
                        return
                    self.field.sqsize = int(self.field.sqsize * (1.1 ** e.y))
        self.field.update(self.game.actions)

        self.render()

    def render(self):
        # rendering
        self.field.under_draw_iterate_cells()
        self.field.draw_shadows()
        self.field.cover_draw_iterate_cells()
        self.game.face_button.update_n_draw(self.game.win_width / 2 - BUTTON_SPACING - BUTTON_IMGS[0].get_width(),
                                    SIDEBAR_HEIGHT / 2, ycentred=True, text=self.emoticon)
        self.game.counters.update_n_render()


class WinYay(State):
    def __init__(self, game):
        super().__init__(game)

    def update(self, events):
        # previous state is still rendered
        self.game.current_states[-2].render()
        self.game.field.update(self.game.actions)



class Lose(State):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.music.load(LOSE_MUSIC)
        pygame.mixer.music.play(start=38.25)
        get_square_size(self.game.field.sqsize)
        self.game.explosions = []
        self.game.explosions.append(Explosion(game, self.game.m_row, self.game.m_col, first_mine=True))


    def update(self, events):  # do animations or smt

        # rendering
        #self.game.field.layer2_draw()
        self.game.field.under_draw_iterate_cells()
        for explosion in self.game.explosions:
            explosion.update()
        self.game.field.draw_shadows()
        self.game.field.cover_draw_iterate_cells()
        self.game.face_button.update_n_draw(self.game.win_width / 2 - BUTTON_SPACING - BUTTON_IMGS[0].get_width(),
                                            SIDEBAR_HEIGHT / 2, ycentred=True, text=LOSE_FACE)
        self.game.counters.update_n_render()


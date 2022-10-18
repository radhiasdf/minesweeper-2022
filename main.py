# the versioning is a bit ruined
import time

import pygame.time
from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from Minesweeper.states import *
from Minesweeper.gui import *


class Game:
    def __init__(self):
        self.running = True
        self.playing = True
        try:
            self.num_rows, self.num_cols, self.num_mines = user_data["r_c_m"]
        except:
            self.num_rows, self.num_cols, self.num_mines = MEDIUM

        pygame.init()
        pygame.display.set_caption("minesweeper WITH BIRCH SIGNS")
        pygame.display.set_icon(ICON)
        self.win_width, self.win_height = MINSQSIZE * self.num_cols, MINSQSIZE * self.num_rows + SIDEBAR_HEIGHT
        self.win = pygame.display.set_mode((self.win_width, self.win_height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.events = ()
        self.settings = Settings(self)
        self.mousepos = (0, 0)
        """try:
            self.current_states = user_data["last_saved"]
            self.reset(last_saved=True)
        except:"""
        self.reset()

    def reset(self, last_saved=False):
        # figuring out minimum window height and width; put this somewhere else; replace literals
        if self.num_cols < 10:
            width = 10
        else:
            width = self.num_cols
        if self.num_rows < 10:
            height = 10
        else:
            height = self.num_rows
        # if not last_saved:
        self.current_states = []
        self.current_states.append(StartPlaying(self))

        # todo: make window resizing more flexible
        self.win_width, self.win_height = MINSQSIZE * width, MINSQSIZE * height + SIDEBAR_HEIGHT
        self.win = pygame.display.set_mode((self.win_width, self.win_height), pygame.RESIZABLE)
        self.face_button = ButtonMC(self, text=IDLE_FACE)



    def game_loop(self):
        prev_time = time.time()
        while self.playing:
            self.dt = time.time() - prev_time
            prev_time = time.time()

            self.events = pygame.event.get()
            for e in self.events:
                if e.type == QUIT:
                    self.running = False
                    self.playing = False
                    return
                if e.type == KEYDOWN:  # pls add a general ingame state to run along with one of the other states or smt rather than using the gameloop
                    if e.key in RESETBUTTON:
                        self.reset()
                if e.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    self.mousepos = pygame.mouse.get_pos()
                    if self.face_button.rect.collidepoint(self.mousepos):
                        CLICK_SOUND.play()
                        self.reset()
                    if self.settings.settingsbutton.rect.collidepoint(self.mousepos):
                        CLICK_SOUND.play()
                        self.settings.open_close()

            # rendering
            self.win.fill(BG_COLOUR)
            self.settings.update(self.events)
            self.current_states[-1].update(self.events)  # majority of input managed here
            pygame.display.update()

            self.clock.tick(FPS)


game = Game()
while game.running:
    game.game_loop()

user_data["r_c_m"] = game.num_rows, game.num_cols, game.num_mines
# user_data["last_saved"] = game.current_states
user_data.close()

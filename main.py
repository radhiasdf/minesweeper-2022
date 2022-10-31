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
        self.sqsize = MINSQSIZE

        pygame.init()
        pygame.display.set_caption("minesweeper WITH BIRCH SIGNS")
        pygame.display.set_icon(ICON)
        self.win_width, self.win_height = self.sqsize * self.num_cols + GRIDXPOS*2, self.sqsize * self.num_rows + GRIDYPOS*2 + SIDEBAR_HEIGHT
        self.win = pygame.display.set_mode((self.win_width, self.win_height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()

        self.events = ()
        self.actions = {"left": False, "right": False, "up": False, "down": False}
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
        self.current_states = []
        self.current_states.append(StartPlaying(self))

        # todo: make window resizing more flexible
        self.win_width, self.win_height = self.sqsize * width, self.sqsize * height + SIDEBAR_HEIGHT
        if self.win_width > MAX_WIN_WIDTH:
            self.win_width = MAX_WIN_WIDTH
        if self.win_height == MAX_WIN_HEIGHT:
            self.win_height = MAX_WIN_HEIGHT
        self.win_width += GRIDXPOS*2
        self.win_height += GRIDXPOS*2

        self.settings.update_positions((self.win_width, 0))
        self.face_button = ButtonMC(self, text=IDLE_FACE)
        self.face_button.reposition(self.win_width / 2 - BUTTON_SPACING - BUTTON_IMGS[0].get_width(),
                                    SIDEBAR_HEIGHT / 2, ycentred=True)
        if self.settings.is_open:
            self.win = pygame.display.set_mode((self.win_width + SETTINGS_WIDTH, self.win_height), pygame.RESIZABLE)
        else:
            self.win = pygame.display.set_mode((self.win_width, self.win_height), pygame.RESIZABLE)

    def game_loop(self):
        prev_time = time.time()
        while self.playing:
            self.dt = time.time() - prev_time
            prev_time = time.time()
            try: print(1/self.dt)
            except: pass

            self.events = pygame.event.get()
            for e in self.events:
                if e.type == QUIT:
                    self.running = False
                    self.playing = False
                    return
                elif e.type == pygame.VIDEORESIZE:
                    self.face_button.reposition(self.win_width / 2 - BUTTON_SPACING - BUTTON_IMGS[0].get_width(),
                    SIDEBAR_HEIGHT / 2, ycentred=True)
                if e.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    self.mousepos = pygame.mouse.get_pos()
                    if self.face_button.rect.collidepoint(self.mousepos):
                        CLICK_SOUND.play()
                        self.reset()
                    if self.settings.settingsbutton.rect.collidepoint(self.mousepos):
                        CLICK_SOUND.play()
                        self.settings.open_toggle()
                if e.type == KEYDOWN: # todo: maybe add a general ingame state to run along with one of the other states or smt rather than using the gameloop. so the gameloop would manage input
                    if e.key in RESETBUTTON:
                        self.reset()
                    if e.key == pygame.K_a:
                        self.actions['left'] = True
                    if e.key == pygame.K_d:
                        self.actions['right'] = True
                    if e.key == pygame.K_w:
                        self.actions['up'] = True
                    if e.key == pygame.K_s:
                        self.actions['down'] = True
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_a:
                        self.actions['left'] = False
                    if e.key == pygame.K_d:
                        self.actions['right'] = False
                    if e.key == pygame.K_w:
                        self.actions['up'] = False
                    if e.key == pygame.K_s:
                        self.actions['down'] = False

            self.win.fill(BG_COLOUR)
            self.current_states[-1].update(self.events)  # majority of input managed here
            self.settings.update(self.events)
            pygame.display.update()

            self.clock.tick(FPS)


game = Game()
while game.running:
    game.game_loop()

user_data["r_c_m"] = game.num_rows, game.num_cols, game.num_mines
# user_data["last_saved"] = game.current_states
user_data.close()

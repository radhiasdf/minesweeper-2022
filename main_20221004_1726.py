#  oh man the versioning is kinda ruined
import time
import pygame.time
from pygame import QUIT, KEYDOWN, MOUSEBUTTONDOWN
from Minesweeper.states import *
from Minesweeper.gui import *


class Game:
    def __init__(self):
        self.running = True
        self.playing = True
        self.num_rows, self.num_cols = 16, 30  # change this to customisable later
        self.num_mines = 9  # There's a mine in every [] squares, 5 is hard, 8 is easy

        pygame.init()
        pygame.display.set_caption("minesweeper WITH BIRCH SIGNS")
        pygame.display.set_icon(ICON)
        self.win_width, self.win_height = MINSQSIZE * self.num_cols, MINSQSIZE * self.num_rows + SIDEBAR_HEIGHT
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        self.clock = pygame.time.Clock()

        self.face_button = ButtonMC(self)

        self.current_states = []  # im not using this effectively
        self.reset()

    def reset(self):
        self.current_states = []
        self.current_states.append(StartPlaying(self))

    def game_loop(self):
        while self.playing:
            self.clock.tick(FPS)
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT:
                    self.running = False
                    self.playing = False
                    return
                if e.type == KEYDOWN:  # pls add a general ingame state to run along with one of the other states rather than using gameloop
                    if e.key in RESETBUTTON:
                        self.reset()
                if e.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and self.face_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.reset()

            if self.face_button.rect.collidepoint(pygame.mouse.get_pos()):
                self.face_button.texture = BUTTON_IMGS[1]
            else: self.face_button.texture = BUTTON_IMGS[0]

            for state in self.current_states:
                state.update(events)
            pygame.display.update()
            #print(self.current_states)


game = Game()
while game.running:
    game.game_loop()

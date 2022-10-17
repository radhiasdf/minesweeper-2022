import time
import pygame
from Minesweeper.grid import *
from Minesweeper.constants import *


class Game:
    def __init__(self):
        self.running = True
        self.playing = True
        self.num_rows, self.num_cols = 16, 30  # change this to customisable later
        self.num_mines = 99  # There's a mine in every [] squares, 5 is hard, 8 is easy

        self.win_width, self.win_height = MINSQSIZE * self.num_cols, MINSQSIZE * self.num_rows + SIDEBAR_HEIGHT
        print(self.win_width, self.win_height)

        pygame.init()
        pygame.display.set_caption("minesweeper WITH BIRCH SIGNS!!!")
        pygame.display.set_icon(ICON)
        self.win = pygame.display.set_mode((self.win_width, self.win_height))
        self.state_stack = []
        self.clicks = 0
        self.start_time = 0
        self.clock = pygame.time.Clock()
        self.coverfield = Coverfield(self.win, self.num_cols, self.num_rows)
        self.underfield = Underfield(self.win, self.num_cols, self.num_rows)
        self.mousepressed = 0

    def game_loop(self):
        self.clicks = 0
        while self.playing:
            self.clock.tick(FPS)
            self.get_events()
            self.update()

    def get_events(self):

        mousepos = pygame.mouse.get_pos()
        row, col = int(mousepos[1] / sqsize), int(mousepos[0] / sqsize)  # assigning xy position to grid

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousepressed = pygame.mouse.get_pressed()
                print(self.mousepressed)
                if self.mousepressed[0]:
                    self.coverfield.highlight(row, col, self.mousepressed)
                else:
                    self.coverfield.editflag(row, col)

            if event.type == pygame.MOUSEBUTTONUP:
                if self.mousepressed[0]:  # left click
                    if self.clicks == 0:
                        self.underfield.generate_data(row, col, self.num_mines)
                        self.start_time = time.time()
                    self.coverfield.reveal(row, col, self.underfield)
                    self.clicks += 1

    def update(self):
        if self.clicks > 0:
            stopwatch = int(time.time() - self.start_time)
        else:
            stopwatch = 0

        self.win.fill(BG_COLOUR)
        self.underfield.draw_checkerboard("white", "gray96")
        self.underfield.draw_data()
        self.coverfield.draw_board("darkolivegreen3", "darkolivegreen3")

        text = SIDEBAR_FONT.render(str(stopwatch), True, "white")
        self.win.blit(text, (10, self.win_height - SIDEBAR_HEIGHT + (SIDEBAR_HEIGHT - text.get_height()) / 2))

        if sum(self.coverfield.field, []).count(concealed) + sum(self.coverfield.field, []).count(
                flagged) == self.underfield.num_mines:
            self.draw_face(WIN_FACE)

        pygame.display.update()

    def draw_face(self, face_text):
        text = SIDEBAR_FONT.render(face_text, True, "white")
        self.win.blit(text, (self.win_width - text.get_width() - 10,
                             self.win_height - SIDEBAR_HEIGHT + (SIDEBAR_HEIGHT - text.get_height()) / 2))

    def lose(self):
        print('nnnnnnnnnoooooooooooo')


game = Game()
while game.running:
    game.game_loop()

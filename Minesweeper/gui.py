# i definitely need to fundamentally change how the gui works calculating the positions so the buttons etc are flexibly arranged one after another

from .constants import *
import time


class ButtonMC:
    def __init__(self, game, text=''):
        self.set_text = text
        self.game = game
        self.texture = BUTTON_IMGS[0]
        self.rect = self.texture.get_rect()

    def update_n_draw(self, xpos, ypos, xcentred=False, ycentred=False, text=''):
        if xcentred:
            xpos = xpos - (self.texture.get_width() / 2)
        if ycentred:
            ypos = ypos - (self.texture.get_height() / 2)
        self.rect[0], self.rect[1] = xpos, ypos

        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.texture = BUTTON_IMGS[1]
        else:
            self.texture = BUTTON_IMGS[0]

        self.game.win.blit(self.texture, (self.rect[0], self.rect[1]))
        if self.set_text != '':  # the optional text argument in draw() would overwrite the text set at the beginning
            if text == '':
                text = self.set_text
            text = SIDEBAR_FONT.render(text, True, "gray20")
            self.game.win.blit(text, (self.rect[0] + (self.texture.get_width() - text.get_width()) / 2,
                                      self.rect[1] + (self.texture.get_height() - text.get_height()) / 2))


# the stopwatch and flag count are in one class
class Counters:
    def __init__(self, game):
        self.game = game
        self.stopwatch = 0
        self.start_time = 0
        self.time_started = False
        self.stopwatch_paused = False
        self.flag_count = game.num_mines

    def reset_stopwatch(self):
        self.start_time = time.time()
        self.time_started = True

    def update_n_render(self):
        # stopwatch
        if self.time_started and not self.stopwatch_paused:
            self.stopwatch = int(time.time() - self.start_time)

        text = SIDEBAR_FONT.render(str(self.stopwatch), True, "white")
        self.game.win.blit(text, (self.game.win_width - text.get_width() - COUNTER_PADDING,
                                  (SIDEBAR_HEIGHT - text.get_height()) / 2))

        # flag count
        text = SIDEBAR_FONT.render(str(self.flag_count), True, "white")
        self.game.win.blit(text, (COUNTER_PADDING, (SIDEBAR_HEIGHT - text.get_height()) / 2))


# for inputting customised row col and mines
class TextInputBox:
    def __init__(self, win):
        self.win = win
        self.selected = False
        self.colour_unselected = 'gray30'
        self.colour_selected = 'white'
        self.colour = self.colour_unselected
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.text = ''

    def draw(self, xpos, ypos, width, height):
        self.rect = pygame.Rect(xpos, ypos, width, height)
        text_x_offset = 7
        if self.selected:
            self.colour = self.colour_selected
        else:
            self.colour = self.colour_unselected
        # draw box
        box = pygame.draw.rect(self.win, self.colour, self.rect, 2)
        # draw text
        rendered_text = SETTINGS_FONT.render(str(self.text), True, 'white')
        self.win.blit(rendered_text, (self.rect.x + text_x_offset, self.rect.y))
        if self.selected:
            # text cursor
            pygame.draw.line(self.win, 'white',
                             (self.rect.x + rendered_text.get_width() + text_x_offset, self.rect.y + box.h / 5),
                             (self.rect.x + rendered_text.get_width() + text_x_offset, self.rect.y + box.h - box.h / 5))


# adds the settings button itself, and everything in the settings menu
class Settings:
    def __init__(self, game):
        self.game = game
        self.is_open = False
        self.buttons = []
        self.settingsbutton = ButtonMC(game, text='S')
        # default mode buttons
        self.modebuttons = []
        for i in range(len(MODES)):
            current = ButtonMC(self.game, text=MODES[i][0])
            self.modebuttons.append(current)
            self.buttons.append(current)

        # to show and/or input row col mines
        self.textboxes = []
        for _ in range(len(PARAMETERS)):
            self.textboxes.append(TextInputBox(self.game.win))
        self.textboxes[0].text = str(self.game.num_rows)
        self.textboxes[1].text = str(self.game.num_cols)
        self.textboxes[2].text = str(self.game.num_mines)
        # enter button for user inputted row col mines
        self.enterbutton = ButtonMC(game, text=ENTER_SYM)
        self.buttons.append(self.enterbutton)

    def open_close(self):
        if self.is_open:
            self.is_open = False
            pygame.display.set_mode((self.game.win_width, self.game.win_height), pygame.RESIZABLE)
        else:
            self.is_open = True
            pygame.display.set_mode((self.game.win_width + SETTINGS_WIDTH, self.game.win_height), pygame.RESIZABLE)

    def update(self, events):
        mousepos = pygame.mouse.get_pos()

        self.settingsbutton.update_n_draw(self.game.win_width / 2 + BUTTON_SPACING,
                                          (SIDEBAR_HEIGHT / 2),
                                          ycentred=True)
        if self.is_open:
            try:
                rows = int(self.textboxes[0].text)
                if rows > MAX_ROWS:
                    rows = MAX_ROWS
                    self.textboxes[0].text = str(rows)
            except: pass
            try:
                cols = int(self.textboxes[1].text)
                if cols > MAX_COLS:
                    cols = MAX_COLS
                    self.textboxes[1].text = str(cols)
            except: pass
            try:
                mines = int(self.textboxes[2].text)
                if mines > rows * cols:
                    mines = rows * cols
                    self.textboxes[2].text = str(mines)
            except: pass

            for e in events:
                if e.type == pygame.MOUSEBUTTONDOWN:
                    for i in range(len(self.textboxes)):  # 6/10/2022 there was a bug where only the last textbox cant be set to true, this is bc teh for loop resets them to unselected except at the end
                        if self.textboxes[i].rect.collidepoint(mousepos):
                            self.textboxes[i].selected = True
                        else:
                            self.textboxes[i].selected = False
                    for i in range(len(self.buttons)):
                        if self.buttons[i].rect.collidepoint(mousepos):
                            CLICK_SOUND.play()
                            # sets textbox texts into the clicked default mode
                            for j in range(len(MODES)):
                                if self.buttons[i].set_text == MODES[j][0]:
                                    for k in range(len(self.textboxes)):
                                        self.textboxes[k].text = str(MODES[j][1][k])
                            # parameters for the grid are set
                            if self.buttons[i].set_text == ENTER_SYM:
                                try:
                                    self.game.num_rows = rows
                                    self.game.num_cols = cols
                                    self.game.num_mines = mines
                                    self.game.reset()
                                except:
                                    pass

                if e.type == pygame.KEYDOWN:
                    for box in self.textboxes:
                        if box.selected:
                            if e.unicode.isdigit():
                                box.text += e.unicode
                            elif e.key == pygame.K_BACKSPACE:
                                box.text = box.text[:-1]
                            elif e.key == pygame.K_RETURN:
                                box.selected = False

            # rendering buttons with updated positions. positions need to be changed to anchor to settings position
            for i in range(len(MODES)):
                self.modebuttons[i].update_n_draw(i * BUTTON_IMGS[0].get_width() + self.game.win_width + GUI_PADDING,
                                                  GUI_PADDING)
            self.enterbutton.update_n_draw(self.textboxes[-1].rect.x + self.textboxes[-1].rect.width + GUI_PADDING,
                                           self.textboxes[-1].rect.y)

            # rendering textboxes, their ypos coded to come after buttons plus their row col mines title
            for i in range(len(self.textboxes)):
                xpos = i * (TEXTBOX_WIDTH + GUI_PADDING) + GUI_PADDING + self.game.win_width
                ypos = self.buttons[0].texture.get_height() + SMALL_FONT.get_height() * 2

                # the mines textbox is slightly wider
                textbox_width = TEXTBOX_WIDTH
                if i == 2: textbox_width = TEXTBOX_WIDTH + SETTINGS_FONT.get_height()
                self.textboxes[i].draw(xpos, ypos, textbox_width, SETTINGS_FONT.get_height() * 1.5)

                # word describing what each textbox is for
                rendered_text = SMALL_FONT.render(str(PARAMETERS[i]), True, 'gray70')
                self.game.win.blit(rendered_text, (xpos + 2, ypos - self.textboxes[i].rect.h/2 - 2))
            # mine frequency indicator
            try:
                rarity = str(round((rows * cols)/mines, 1))
                rendered_text = SMALL_FONT.render("1 mine every " + rarity + " squares", True, 'gray70')
                self.game.win.blit(rendered_text, (self.game.win_width + GUI_PADDING, self.buttons[0].texture.get_height() + SMALL_FONT.get_height()*2 + SETTINGS_FONT.get_height() * 1.5 + 2))
            except:
                pass


import pygame
import shelve
user_data = shelve.open("user_data")
#user_data["r_c_m"] = (16, 16, 40)  # setting up default for user data?

pygame.init()

BG_COLOUR = "black"
FPS = 60
TARGET_FPS = 60
MAX_WIN_WIDTH, MAX_WIN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
print(MAX_WIN_WIDTH, MAX_WIN_HEIGHT)
MINSQSIZE = 16  # the original minesweeper square size is around 16
SIDEBAR_HEIGHT = 50
GRIDXPOS = 0
GRIDYPOS = 50
SETTINGS_POS = ()
SETTINGS_WIDTH = 250
BUTTON_SPACING = 0
GUI_PADDING = 5
COUNTER_PADDING = 10
TEXTBOX_WIDTH = 50

IDLE_FACE = ":)"
MOUSEDOWN_FACE = ":o"
WIN_FACE = "B)"
LOSE_FACE = "X("
ENTER_SYM = '>'

RESETBUTTON = [pygame.K_F2]

PARAMETERS = ('rows', 'cols', 'mines')
EASY = (9, 9, 10)  # rows, cols, mines
MEDIUM = (16, 16, 40)
EXPERT = (16, 30, 99)
MODES = [['E', EASY],
         ['M', MEDIUM],
         ['H', EXPERT]]
MAX_ROWS, MAX_COLS = 35, 60  # change this to fit max win width win height

#  some shader thingy
SHADOW_COLOUR = "black"
# very limited
THREE_D_OFFSET_X = 0
THREE_D_OFFSET_Y = MINSQSIZE * 0.13

# images
ICON = pygame.transform.scale(pygame.image.load("assets/Birch_Sign_JE1_BE1.png"), (32, 32))
MINE_IMG = pygame.transform.scale(pygame.image.load('assets/TNT_ 28top_texture 29_JE2_BE2.png'), (MINSQSIZE, MINSQSIZE))
SIGN_IMG = pygame.transform.scale(pygame.image.load('assets/Birch_Sign_JE1_BE1.png'), (MINSQSIZE, MINSQSIZE))
COVER_IMG = pygame.transform.scale(pygame.image.load('assets/Grass_Block_29_JE4_BE2.png'), (MINSQSIZE, MINSQSIZE))
LOWER_CELL_IMG = pygame.transform.scale(pygame.image.load('assets/Sand_ 28texture 29_JE5_BE3.png'),
                                        (MINSQSIZE, MINSQSIZE))
BUTTON_IMGS = [pygame.transform.scale(pygame.image.load('assets/mc_generalised_button.png'), (40, 36)),
               pygame.transform.scale(pygame.image.load('assets/mc_generalised_button_hover.png'), (40, 36))]
# animations
EXPLOSIONS = []
for i in range(15):
    EXPLOSIONS.append(pygame.transform.scale(
        pygame.image.load(f"assets/explosion/explosion_{i+1}.png"), (MINSQSIZE*3, MINSQSIZE*3)))

# fonts
BOLD_FONT = pygame.font.Font('assets/MinecraftBold-nMK1.ttf', int(MINSQSIZE))
NUM_FONT = pygame.font.Font('assets/MinecraftRegular-Bmg3.ttf', int(MINSQSIZE))
SIDEBAR_FONT = pygame.font.Font('assets/MinecraftRegular-Bmg3.ttf', 22)  # pls make the pixel size consistent
SETTINGS_FONT_SIZE = 22
SETTINGS_FONT = pygame.font.Font('assets/MinecraftRegular-Bmg3.ttf', SETTINGS_FONT_SIZE)
SMALL_FONT_SIZE = 16
SMALL_FONT = pygame.font.Font('assets/MinecraftRegular-Bmg3.ttf', SMALL_FONT_SIZE)

NUM_COLOURS = {1: "blue", 2: "darkgreen", 3: "red", 4: "darkblue", 5: "darkred", 6: "darkcyan", 7: "black",
               8: "dimgray"}

# audio
CLICK_SOUND = pygame.mixer.Sound("assets/click.ogg")
DIG_SOUNDS = [pygame.mixer.Sound(f"assets/sand{i + 1}.ogg") for i in range(3)]
EXPLODE_SOUNDS = [pygame.mixer.Sound(f"assets/explode{i+1}.ogg") for i in range(4)]
FLAG_SOUNDS = [pygame.mixer.Sound(f"assets/wood{i + 1}.ogg") for i in range(4)]

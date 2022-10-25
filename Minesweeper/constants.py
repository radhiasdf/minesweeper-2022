import pygame
import shelve


def changeColour(image, colour, special_flags=pygame.BLEND_MULT):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(colour)

    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags=special_flags)
    return finalImage

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
GRIDXPOS = 5
GRIDYPOS = SIDEBAR_HEIGHT
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

# input
RESETBUTTON = [pygame.K_F2]
GRID_MOVE_SPEED = 100

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
THREE_D_OFFSET_X = MINSQSIZE * 0
THREE_D_OFFSET_Y = MINSQSIZE * 0.13

# images
ICON = pygame.transform.scale(pygame.image.load("assets/Birch_Sign_JE1_BE1.png"), (32, 32))
BUTTON_IMGS = [pygame.transform.scale(pygame.image.load('assets/mc_generalised_button.png'), (40, 36)),
               pygame.transform.scale(pygame.image.load('assets/mc_generalised_button_hover.png'), (40, 36))]

MINE_IMG = pygame.image.load('assets/TNT_ 28top_texture 29_JE2_BE2.png')
MINE_IMG_BRIGHT = changeColour(MINE_IMG, (255,255,255), special_flags=pygame.BLEND_RGB_ADD)  # not perfect, i havent succeded in making a white overlay
MINE_IMG = pygame.transform.scale(MINE_IMG, (MINSQSIZE, MINSQSIZE))
MINE_IMG_BRIGHT = pygame.transform.scale(MINE_IMG_BRIGHT, (MINSQSIZE, MINSQSIZE))


FLAG_IMG = pygame.image.load('assets/Birch_Sign_JE1_BE1.png')
COVER_IMG = pygame.image.load('assets/Grass_Block_29_JE4_BE2.png')
LOWER_CELL_IMG = pygame.image.load('assets/Sand_ 28texture 29_JE5_BE3.png')

# animations
EXPLOSION_PARTICLES = []
for i in range(15):
    EXPLOSION_PARTICLES.append(pygame.image.load(f"assets/explosion/explosion_{i+1}.png"))

# fonts
BOLD_FONT = 'assets/MinecraftBold-nMK1.ttf'
DEFAULT_FONT = 'assets/MinecraftRegular-Bmg3.ttf'
SIDEBAR_FONT = pygame.font.Font(DEFAULT_FONT, 22)  # pls make the pixel size consistent
SETTINGS_FONT = pygame.font.Font(DEFAULT_FONT, 22)
SMALL_FONT = pygame.font.Font(DEFAULT_FONT, 16)

NUM_COLOURS = {1: "blue", 2: "darkgreen", 3: "red", 4: "darkblue", 5: "darkred", 6: "darkcyan", 7: "black",
               8: "dimgray"}

# audio
CLICK_SOUND = pygame.mixer.Sound("assets/sounds/click.ogg")
DIG_SOUNDS = [pygame.mixer.Sound(f"assets/sounds/sand{i + 1}.ogg") for i in range(3)]
EXPLODE_SOUNDS = [pygame.mixer.Sound(f"assets/sounds/explode{i+1}.ogg") for i in range(4)]
for sound in EXPLODE_SOUNDS:
    sound.set_volume(0.4)
FLAG_SOUNDS = [pygame.mixer.Sound(f"assets/sounds/wood{i + 1}.ogg") for i in range(4)]
LOSE_MUSIC = 'assets/sounds/[YT2mp3.info] - C418 - Stal (Minecraft Volume Beta) (256kbps).mp3'
WIN_MUSIC = 'assets/sounds/[YT2mp3.info] - C418 - Door - Minecraft Volume Alpha (320kbps).mp3'
pygame.mixer.music.set_volume(0.4)
EXPLODE_RADIUS = 4
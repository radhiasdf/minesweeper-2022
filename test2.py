import pygame, sys

SCREEN_SIZE = (600, 400)
BG_COLOR = (0, 0, 0)
LINE_COLOR = (0, 255, 0)
pygame.init()
clock = pygame.time.Clock() # to keep the framerate down

image1 = pygame.Surface((50, 50))
image2 = pygame.Surface((50, 50))
image1.set_colorkey((0, 0, 0)) # The default background color is black
image2.set_colorkey((0, 0, 0)) # and I want drawings with transparency

screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
screen.fill(BG_COLOR)

# Draw to two different images off-screen
pygame.draw.line(image1, LINE_COLOR, (0, 0), (49, 49))
pygame.draw.line(image2, LINE_COLOR, (49, 0), (0, 49))

# Optimize the images after they're drawn
image1.convert()
image2.convert()

# Get the area in the middle of the visible screen where our images would fit
draw_area = image1.get_rect().move(SCREEN_SIZE[0] / 2 - 25,
                                   SCREEN_SIZE[1] / 2 - 25)

# Draw our two off-screen images to the visible screen
screen.blit(image1, draw_area)
screen.blit(image2, draw_area)

# Display changes to the visible screen
pygame.display.flip()
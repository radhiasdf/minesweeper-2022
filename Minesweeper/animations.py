import random
import pygame.surface
from Minesweeper.constants import EXPLOSIONS, MINSQSIZE

#  masks the image to a different colour
def changeColour(image, colour):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(colour)

    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags=pygame.BLEND_MULT)
    return finalImage


class BoomAnimator:
    def __init__(self, game):
        self.game = game
        self.last_update = 0
        self.particles = []

        self.radius = 4
        self.num_particles = 20

    def update(self):
        # to make the particles start at different times
        if len(self.particles) < self.num_particles:
            self.particles.append(ExplosionParticle(self.game, self.game.mousepos[0] - EXPLOSIONS[0].get_width() / 2 + random.randint(-(self.radius - 1) * MINSQSIZE, (self.radius - 1) * MINSQSIZE)
                                                    , self.game.mousepos[1] - EXPLOSIONS[0].get_height() / 2 + random.randint(-(self.radius - 1) * MINSQSIZE, (self.radius - 1) * MINSQSIZE)))
        for p in self.particles:
            p.frame_index += p.animation_speed * self.game.dt  # framerate independence
            if p.frame_index >= len(EXPLOSIONS):
                p.frame_index = 0

            p.update()


class ExplosionParticle:
    def __init__(self, game, x, y):
        self.animation_speed = 60
        self.frame_index = 0
        self.game = game
        self.x, self.y = x, y
        self.colour = f"gray{random.randint(50, 100)}"

    def update(self):
        image = changeColour(EXPLOSIONS[int(self.frame_index)], self.colour)
        self.game.win.blit(image, (self.x, self.y))




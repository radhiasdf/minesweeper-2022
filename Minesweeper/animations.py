import random
import pygame.surface
from Minesweeper.constants import EXPLOSIONS, MINSQSIZE, EXPLODE_RADIUS, EXPLODE_SOUNDS, MINE_IMG


#  masks the image to a different colour
def changeColour(image, colour, special_flags=pygame.BLEND_MULT):
    colouredImage = pygame.Surface(image.get_size())
    colouredImage.fill(colour)

    finalImage = image.copy()
    finalImage.blit(colouredImage, (0, 0), special_flags=special_flags)
    print('hello')
    return finalImage


class Explosion:
    def __init__(self, game, centre_r, centre_c, first_mine=False):
        self.game = game
        self.ypos = centre_r * MINSQSIZE
        self.xpos = centre_c * MINSQSIZE
        self.centre_r = centre_r
        self.centre_c = centre_c
        self.game.field.field[self.centre_r][self.centre_c].mine = False  # to prevent duplicate mine triggering
        self.flashToggle = True
        self.particles = []
        if first_mine:
            self.numParticles = 20  # constant
            self.pSpawnInterval = 1 / 60  # in seconds
        else:
            self.numParticles = 1
            self.pSpawnInterval = 1 / 10
        self.fuseTime = 1
        self.flashInterval = 0.2
        self.fusing = True
        self.timer = 0
        self.timer2 = 0
        # radius decreased by one square so the particles rnt so off the edge. also random randint is in range of
        # pixels, not cells, so the particle places r more random
        self.radiusInPixels = (EXPLODE_RADIUS - 1) * MINSQSIZE

    def update(self):
        if self.fusing:
            self.draw_mine()
            self.timer += self.game.dt
            self.timer2 += self.game.dt
            if self.timer2 >= self.flashInterval:
                self.flashToggle ^= True
                self.timer2 = 0
            if self.timer >= self.fuseTime:
                self.fusing = False
                self.timer = 0
                EXPLODE_SOUNDS[random.randint(0, len(EXPLODE_SOUNDS) - 1)].play()
                # makes some circular hole from the explosion
                cells_in_exploded_circle = self.game.field.get_cells_in_circle(self.centre_r, self.centre_c,
                                                                               EXPLODE_RADIUS)
                for r, c in cells_in_exploded_circle:
                    self.game.field.field[r][c].revealed = True
                    # chain reaction of explosions
                    if self.game.field.field[r][c].mine:
                        self.game.explosions.append(Explosion(self.game, r, c))
            return
        # to make the particles start at different times. this is a bit convoluted for a single explosion that would
        # be summoned for every mine
        if len(self.particles) < self.numParticles:
            self.timer += self.game.dt
            if self.timer >= self.pSpawnInterval:
                self.particles.append(
                    ExplosionParticle(self.game, self.xpos + random.randint(-self.radiusInPixels, self.radiusInPixels),
                                      self.ypos + random.randint(-self.radiusInPixels, self.radiusInPixels)))
                # self.particles.append(ExplosionParticle(self.game, self.xpos, self.ypos))
                self.timer = 0
        # iterating through the images
        for p in self.particles:
            p.frameIndex += p.animationSpeed * self.game.dt  # framerate independence
            if p.frameIndex >= len(EXPLOSIONS):
                del p
            else:
                p.update()

    def draw_mine(self):
        if self.flashToggle:
            image = changeColour(MINE_IMG, "white", special_flags=pygame.BLEND_ALPHA_SDL2)
        else: image = MINE_IMG
        self.game.win.blit(image, (self.centre_c * MINSQSIZE + (MINSQSIZE - MINE_IMG.get_width()) / 2,
                                      self.centre_r * MINSQSIZE + (MINSQSIZE - MINE_IMG.get_height()) / 2))


class ExplosionParticle:
    # the location of each particle is randomly determined by boom animator
    def __init__(self, game, x, y):
        self.animationSpeed = 60
        self.frameIndex = 0
        self.game = game
        self.x, self.y = x, y
        self.colour = f"gray{random.randint(50, 100)}"

    def update(self):
        image = changeColour(EXPLOSIONS[int(self.frameIndex)], self.colour)
        self.game.win.blit(image, (self.x, self.y))

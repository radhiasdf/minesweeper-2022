import random
import pygame.surface
from Minesweeper.constants import EXPLOSION_PARTICLES, MINSQSIZE, EXPLODE_RADIUS, EXPLODE_SOUNDS, MINE_IMG, MINE_IMG_BRIGHT, changeColour
radiusInPixels = (EXPLODE_RADIUS - 1)


class Explosion:
    def __init__(self, game, centre_r, centre_c, first_mine=False):
        self.game = game
        self.sqsize = game.field.sqsize
        self.centre_r = centre_r
        self.centre_c = centre_c
        self.xpos = self.centre_c * game.field.sqsize + game.field.xpos
        self.ypos = self.centre_r * game.field.sqsize + game.field.ypos
        self.game.field.field[self.centre_r][self.centre_c].mine = False  # to prevent duplicate mine triggering
        self.flashToggle = True
        self.particles = []
        if first_mine:
            self.numParticles = 20  # constant
            self.pSpawnInterval = 1 / 120  # in seconds
            self.fuseTime = 0.7
        else:
            self.numParticles = 1
            self.pSpawnInterval = 1 / 10
            self.fuseTime = 120/103.9  # to make it in sync with the music #random.randint(5,15)/10
        self.flashInterval = 0.2
        self.fusing = True
        self.timer = 0
        self.timer2 = 0

        self.mineImg = pygame.transform.scale(MINE_IMG, (self.sqsize, self.sqsize)).convert_alpha()
        self.mineImgBright = pygame.transform.scale(MINE_IMG_BRIGHT, (self.sqsize, self.sqsize)).convert_alpha()
        self.particleImgs = [pygame.transform.scale(img, (self.sqsize*3, self.sqsize*3)).convert_alpha() for img in EXPLOSION_PARTICLES]
        self.radiusInPixels = radiusInPixels * self.sqsize

        # radius decreased by one square so the particles rnt so off the edge. also random randint is in range of
        # pixels, not cells, so the particle places r more random

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
                self.particles.append(ExplosionParticle(self.game, self.xpos, self.ypos, self.particleImgs, self.radiusInPixels))
                self.timer = 0
        # iterating through the images
        for p in self.particles:
            p.frameIndex += p.animationSpeed * self.game.dt  # framerate independence
            if p.frameIndex >= len(EXPLOSION_PARTICLES):
                del p
            else:
                p.update()

    def draw_mine(self):
        if self.flashToggle:
            image = self.mineImgBright
        else: image = self.mineImg
        self.game.win.blit(image, (self.xpos, self.ypos))


class ExplosionParticle:
    # the location of each particle is randomly determined by boom animator
    def __init__(self, game, xpos, ypos, imgs, radius_in_pixels):
        self.animationSpeed = 60
        self.frameIndex = 0
        self.game = game
        self.xpos = xpos
        self.ypos = ypos
        self.colour = f"gray{random.randint(50, 100)}"
        self.randomXOffset = random.randint(-radius_in_pixels, radius_in_pixels)
        self.randomYOffset = random.randint(-radius_in_pixels, radius_in_pixels)
        self.imgs = imgs

    def update(self):
        self.image = changeColour(self.imgs[int(self.frameIndex)], self.colour)
        self.game.win.blit(self.image, (self.xpos + self.randomXOffset, self.ypos + self.randomYOffset))

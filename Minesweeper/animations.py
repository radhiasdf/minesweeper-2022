import random
import pygame.surface
from .constants import EXPLOSION_PARTICLES, EXPLODE_RADIUS, EXPLODE_SOUNDS, FLAG_SOUNDS,\
    MINE_IMG, MINE_IMG_BRIGHT, FLAG_IMGS, change_colour
radiusInPixels = (EXPLODE_RADIUS - 1)


class WinAnimator:
    def __init__(self, game):
        self.game = game
        self.sqsize = game.field.sqsize
        self.flagImgs = [pygame.transform.scale(img, (self.sqsize, self.sqsize)).convert_alpha() for img in FLAG_IMGS]
        self.rowCols = []
        self.released = []
        for row in range(self.game.num_rows):
            for col in range(self.game.num_cols):
                if self.game.field.field[row][col].mine:
                    self.rowCols.append((row, col))
        self.nextReleaseTimer = 0
        self.updateTimer = 0

    def update(self):
        if len(self.rowCols) > 0:
            self.nextReleaseTimer -= self.game.dt
            if self.nextReleaseTimer <= 0:
                self.nextReleaseTimer = random.uniform(0.5, 1)
                chosen_row_col = self.rowCols.pop(random.randint(0, len(self.rowCols)-1))
                self.released.append(AnimatedFlag(self.game, chosen_row_col,
                                                  (random.uniform(-1.0*60, 1.0*60), random.uniform(-2.0*60, -1.0*60)), self.flagImgs[0]))
                FLAG_SOUNDS[random.randint(0, len(FLAG_SOUNDS))-1].play()
                self.game.field.field[chosen_row_col[0]][chosen_row_col[1]].flagged = 'plucked'

        for flag in self.released:
            flag.update()
class AnimatedFlag:
    def __init__(self, game, row_col, vel, img):
        self.game = game
        self.revealed = True
        self.position = (row_col[1] * game.field.sqsize + game.field.xpos, row_col[0] * game.field.sqsize + game.field.ypos)
        self.trailPositions = []
        self.velocity = vel
        self.acceleration = 1000
        self.img = img

    def update(self):
        self.game.win.blit(self.img, self.position)

        self.velocity = (self.velocity[0], self.velocity[1] + self.acceleration*self.game.dt)
        self.position = (self.position[0] + self.velocity[0]*self.game.dt, self.position[1] + self.velocity[1]*self.game.dt)
        if self.position[0] < 0 - self.img.get_height() or self.position[0] > self.game.win_width or \
                self.position[1] >= self.game.win_height + self.velocity[1]:
            del self
            return
        if self.position[1] >= self.game.win_height - self.img.get_height() and self.velocity[1] > 0:
            self.velocity = (self.velocity[0], -(self.velocity[1]) * .9)



class Explosion:
    def __init__(self, game, centre_r, centre_c, first_mine=False):
        self.game = game
        self.sqsize = game.field.sqsize
        self.centre_r = centre_r
        self.centre_c = centre_c
        self.xpos = self.centre_c * game.field.sqsize + game.field.xpos
        self.ypos = self.centre_r * game.field.sqsize + game.field.ypos
        self.game.field.field[self.centre_r][self.centre_c].mine = False  # to prevent recursion error from infinite mine triggering
        self.flashToggle = True
        self.particles = []
        if first_mine:
            self.numParticles = 20  # constant
            self.pSpawnInterval = 1 / 120  # in seconds
            self.fuseTime = 0.7
        else:
            self.numParticles = 5
            self.pSpawnInterval = 1 / 120
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
                self.particles.append(ExplosionParticle(self.game.win, self.xpos, self.ypos, self.particleImgs, self.radiusInPixels))
                self.timer = 0
        # iterating through the images
        for p in self.particles:
            p.frameIndex += p.animationSpeed * self.game.dt  # framerate independence
            if p.frameIndex >= len(EXPLOSION_PARTICLES):
                del p
            else:
                p.update()
        if len(self.particles) == 0:
            del self

    def draw_mine(self):
        if self.flashToggle:
            image = self.mineImgBright
        else: image = self.mineImg
        self.game.win.blit(image, (self.xpos, self.ypos))


class ExplosionParticle:
    # the location of each particle is randomly determined by boom animator
    def __init__(self, win, xpos, ypos, imgs, radius_in_pixels):
        self.animationSpeed = 60
        self.frameIndex = 0
        self.win = win
        self.xpos = xpos
        self.ypos = ypos
        self.colour = f"gray{random.randint(50, 100)}"
        self.randomXOffset = random.randint(-radius_in_pixels, radius_in_pixels)
        self.randomYOffset = random.randint(-radius_in_pixels, radius_in_pixels)
        self.imgs = imgs

    def update(self):
        self.image = change_colour(self.imgs[int(self.frameIndex)], self.colour)
        self.win.blit(self.image, (self.xpos + self.randomXOffset, self.ypos + self.randomYOffset))

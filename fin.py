import pygame as pg
import pygame
import random
from settings import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()
running = True

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for plat in PLATFORM_LIST:
    p = Platform(*plat)
    all_sprites.add(p)
    platforms.add(p)

def events():
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			if playing:
				playing = False
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.jump()

def update():
	all_sprites.update()
	if player.vel.y > 0:
		hits = pygame.sprite.spritecollide(player, platforms, False)
		if hits:
			player.pos.y = hits[0].rect.top
			player.vel.y = 0

def draw():
	screen.fill(BLACK)
	all_sprites.draw(screen)
	pygame.display.flip()

playing = True
while running:
    clock.tick(FPS)
    events()
    update()
    draw()



pygame.quit()
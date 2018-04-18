import pygame
from settings import *
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
running = True

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self,posx,posy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(posx, posy)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.move_d=False
        self.move_g=False

    def jump(self):
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)

        if bullet.vel.x >= 0:
            self.speedx = 10
        elif self.vel.x < 0:
        	bullet.speedx = -10

        all_sprites.add(bullet)

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)

        if self.move_g:
            self.acc.x = -PLAYER_ACC
        if self.move_d:
            self.acc.x = PLAYER_ACC

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x

    def update(self):
        self.rect.x += self.speedx

        if self.rect.x < 0:
            self.kill()

        if self.rect.x > WIDTH:
            self.kill()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
player = Player(WIDTH/4,HEIGHT/2)
player2 = Player((WIDTH/4)*3,HEIGHT/2)
all_sprites.add(player)
for plat in PLATFORM_LIST:
    p = Platform(*plat)
    all_sprites.add(p)
    platforms.add(p)

def events():
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.move_d=True
            else :
                player.move_d=False

            if event.key == pygame.K_LEFT:
                player.move_g=True
            else :
                player.move_g=False

            if event.key == pygame.K_UP:
                player.jump()
            if event.key == pygame.K_SPACE:
                player.shoot()

def test(player):

    if player.vel.y > 0:
        hits = pygame.sprite.spritecollide(player, platforms, False)
        if hits:
            player.pos.y = hits[0].rect.top
            player.vel.y = 0

    if player.rect.top <= HEIGHT / 4:
        player.pos.y += abs(player.vel.y)
        for plat in platforms:
            plat.rect.y += abs(player.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    if player.rect.bottom > HEIGHT:
        for sprite in all_sprites:
            sprite.rect.y -= max(player.vel.y, 10)
            if sprite.rect.bottom < 0:
                sprite.kill()
    if len(platforms) == 0:
        running = False

def update():
	all_sprites.update()
	test(player)

def draw():
	screen.fill(BLACK)
	all_sprites.draw(screen)
	pygame.display.flip()

while running:
    clock.tick(FPS)
    events()
    update()
    draw()



pygame.quit()

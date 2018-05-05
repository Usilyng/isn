import pygame
from settings import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self,posx,posy,life):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(posx, posy)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.move_D = False
        self.move_G = False
        self.life = life

    def move_g(self):
        self.move_G = True

    def stop_move_g(self):
        self.move_G = False

    def move_d(self):
        self.move_D = True

    def stop_move_d(self):
        self.move_D = False

    def jump(self):
        self.rect.x += 1
        hits = pygame.sprite.spritecollide(self, platforms, False)
        self.rect.x -= 1
        if hits:
            self.vel.y = -20

    def shoot(self):

        if self.life > 0:
            if self.vel.x >= 0:
                bullet = Bullet(self.rect.right, self.rect.centery)
                bullet.speedx = 10
            elif self.vel.x < 0:
                bullet = Bullet(self.rect.left, self.rect.centery)
                bullet.speedx = -10

            all_sprites.add(bullet)
            bullets.add(bullet)

    def update(self):
        self.acc = vec(0, GRAV)

        if self.move_G:
            self.acc.x = -PLAYER_ACC
        if self.move_D:
            self.acc.x = PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION

        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0

        self.rect.midbottom = self.pos

class Mob(pygame.sprite.Sprite):
    def __init__(self,posx,posy,life,target):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 40))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.pos = vec(posx, posy)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.life = life
        self.target = target


    def update(self):
        self.acc = vec(0, GRAV)

        if self.pos.x > self.target.pos.x:
            self.acc.x = -MOB_ACC
        if self.pos.x < self.target.pos.x:
            self.acc.x = MOB_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION

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

def damage_bullets(entity):

    touch_bullets = pygame.sprite.spritecollide(entity, bullets, False)
    if touch_bullets:
        entity.life -= 1

    if entity.life <= 0:
        entity.kill()

def damage_mobs(entity):

    touch_mobs = pygame.sprite.spritecollide(entity, mobs, False)
    if touch_mobs:
        entity.life -= 1

    if entity.life <= 0:
        entity.kill()

def colision(entity):

    if entity.vel.y > 0:
        hits = pygame.sprite.spritecollide(entity, platforms, False)
        if hits:
            entity.pos.y = hits[0].rect.top
            entity.vel.y = 0

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
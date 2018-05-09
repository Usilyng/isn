import pygame
from os import path
from settings import *

vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self,posx,posy,skin,life):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(path.join(path.dirname(__file__), 'img'), skin)).convert()
        self.image.set_alpha()
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

    def shoot(self,skin):

        if self.life > 0:
            if self.vel.x >= 0:
                bullet = Bullet(self.rect.right, self.rect.centery, skin)
                bullet.speedx = 10
            elif self.vel.x < 0:
                bullet = Bullet(self.rect.left, self.rect.centery, skin)
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
    def __init__(self,posx,posy,skin,life,target):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(path.join(path.dirname(__file__), 'img'), skin)).convert()
        self.image.set_alpha()
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
    def __init__(self, x, y, skin):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(path.join(path.dirname(__file__), 'img'), skin)).convert()
        self.image.set_alpha()
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
    def __init__(self, x, y, skin):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(path.join(path.join(path.dirname(__file__), 'img'), skin)).convert()
        self.image.set_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Level_builder():
    def __init__(self, level, skin_w, skin_b, skin_p, skin_e, skin_d):
        self.image_W = skin_w
        self.image_B = skin_b
        self.image_P = skin_p
        self.image_E = skin_e
        self.image_D = skin_d

        self.x = 0
        self.y = -42000

        self.map_data = []
        with open(level, 'rt') as f:
            for line in f:
                self.map_data.append(line)
        
    def build_level(self):
        for row in self.map_data:
            for col in row:

                if col == "H":
                    h = Platform(self.x, self.y, self.image_P)
                    all_sprites.add(h)
                    platforms.add(h)

                if col == "W":
                    w = Platform(self.x, self.y, self.image_P)
                    all_sprites.add(w)
                    walls.add(w)

                if col == "B":
                    p = Platform(self.x, self.y, self.image_P)
                    all_sprites.add(p)
                    platforms.add(p)

                if col == "P":
                    p = Platform(self.x, self.y, self.image_P)
                    all_sprites.add(p)
                    platforms.add(p)

                if col == "E":
                    p = Platform(self.x, self.y, self.image_P)
                    all_sprites.add(p)
                    platforms.add(p)

                if col == "D":
                    d = Platform(self.x, self.y-20, self.image_D)
                    p = Platform(self.x, self.y, self.image_P)
                    all_sprites.add(d)
                    all_sprites.add(p)
                    traps.add(d)
                    platforms.add(p)

                self.x += 50
            self.x = 0
            self.y += 40

def damage_bullets(entity):
    touch_bullets = pygame.sprite.spritecollide(entity, bullets, False)
    if touch_bullets:
        entity.life -= 1
        touch_bullets[0].kill()

    if entity.life <= 0:
        entity.kill()

def damage_mobs(entity):
    touch_mobs = pygame.sprite.spritecollide(entity, mobs, False)
    if touch_mobs:
        entity.life -= 1

    if entity.life <= 0:
        entity.kill()

def damage_traps(entity):
    touch_traps = pygame.sprite.spritecollide(entity, traps, False)
    if touch_traps:
        entity.life -= 1

    if entity.life <= 0:
        entity.kill()

def colision_plat(entity):
    if entity.vel.y > 0:
        hits = pygame.sprite.spritecollide(entity, platforms, False)
        if hits:
            entity.pos.y = hits[0].rect.top
            entity.vel.y = 0

def colision_wall(entity):
    if entity.vel.x < 0:
        hits = pygame.sprite.spritecollide(entity, walls, False)
        if hits:
            entity.pos.x = hits[0].rect.right + (entity.rect.w/2)
            entity.vel.x = 0

    if entity.vel.x > 0:
        hits = pygame.sprite.spritecollide(entity, walls, False)
        if hits:
            entity.pos.x = hits[0].rect.left - (entity.rect.w/2)
            entity.vel.x = 0
    
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
walls = pygame.sprite.Group()
traps = pygame.sprite.Group()
bullets = pygame.sprite.Group()
mobs = pygame.sprite.Group()
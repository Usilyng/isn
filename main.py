import pygame
from settings import *
from moteur import *

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
running = True

player = Player(WIDTH/4,HEIGHT/2,10000000000000000000000)
player2 = Player((WIDTH/4)*3,HEIGHT/2,10000)
mob = Mob(WIDTH-50, HEIGHT/2, 50,player)
mobs.add(mob)
all_sprites.add(player)
all_sprites.add(player2)
all_sprites.add(mob)
for plat in PLATFORM_LIST:
    p = Platform(*plat)
    all_sprites.add(p)
    platforms.add(p)

def events():
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.move_d()

            if event.key == pygame.K_LEFT:
                player.move_g()

            if event.key == pygame.K_UP:
                player.jump()

            if event.key == pygame.K_SPACE:
                player.shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.stop_move_d()

            if event.key == pygame.K_LEFT:
                player.stop_move_g()


    #controle  joueur 2

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player2.move_d()

            if event.key == pygame.K_a:
                player2.move_g()

            if event.key == pygame.K_w:
                player2.jump()

            if event.key == pygame.K_k:
                player2.shoot()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player2.stop_move_d()

            if event.key == pygame.K_a:
                player2.stop_move_g()

def test(player):
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
    colision(player)
    colision(player2)
    colision(mob)
    damage_bullets(player)
    damage_bullets(player2)
    damage_bullets(mob)
    damage_mobs(player)
    damage_mobs(player2)
    test(player)
    test(player2)
    test(mob)

def draw():
	screen.fill(BLACK)
	all_sprites.draw(screen)
	pygame.display.flip()

while running:
    clock.tick(FPS)
    events()
    update()
    draw()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

pygame.quit()
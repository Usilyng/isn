import pygame
from Cavaaller3 import *
from Cavaaller2 import *
import threading
import random
import time

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
running = True

player = Player(WIDTH/4, HEIGHT, "player.png", 10000000000000000000000)
#player2 = Player((WIDTH/4)*3, (HEIGHT/2), "player.png", 10000)
mob = Mob(WIDTH-50, (HEIGHT/2), "mob.png", 50, player)
#final_mob = Mob(WIDTH-30, (HEIGHT/3/2), "mob.png", 50, player2)
mobs.add(mob)
#mobs.add(final_mob)
all_sprites.add(player)
#all_sprites.add(player2)
all_sprites.add(mob)
#all_sprites.add(final_mob)


Levels=["level1.txt", "level2.txt", "level3.txt"]

world = Level_builder(random.choice(Levels), "", "", "plat.png", "plat.png", "trap.png" )
world.build_level()

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
                player.shoot("bulet.png")

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
                player2.shoot("bulet.png")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player2.stop_move_d()

            if event.key == pygame.K_a:
                player2.stop_move_g()

def test(player, mob):

    if player.rect.top <= HEIGHT / 4:
        player.pos.y += abs(player.vel.y)
        for plat in platforms:
            plat.rect.y += abs(player.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    #if player2.rect.top <= HEIGHT / 4:
        #player2.pos.y += abs(player2.vel.y)
        #for plat in platforms:
            #plat.rect.y += abs(player2.vel.y)
            #if plat.rect.top >= HEIGHT:
                #plat.kill()

    if player.rect.bottom > HEIGHT:
        for sprite in all_sprites:
            sprite.rect.y -= max(player.vel.y, 10)
            if sprite.rect.bottom < 0:
                sprite.kill()

    #if player2.rect.bottom > HEIGHT:
        #for sprite in all_sprites:
            #sprite.rect.y -= max(player2.vel.y, 10)
            #if sprite.rect.bottom < 0:
                #sprite.kill()
                
    if len(platforms) == 0:
        playing = False

    if mob.pos.y <= HEIGHT: 
        mob = False

    #if final_mob.pos.y <= HEIGHT: 
        #final_mob = False

    if player.pos.y <= HEIGHT: 
        player = False
        running = True

    #if player2.pos.y <= HEIGHT: 
        #player2 = False
        

def update():
    all_sprites.update()
    colision_plat(player)
    #colision_plat(player2)
    colision_plat(mob)
    #colision_plat(final_mob)
    colision_wall(player)
    #colision_wall(player2)
    colision_wall(mob)
    #colision_wall(final_mob)
    damage_bullets(player)
    #damage_bullets(player2)
    damage_bullets(mob)
    #damage_bullets(final_mob)
    damage_mobs(player)
    #damage_mobs(player2)
    damage_traps(player)
    #damage_traps(player2)
    test(player, mob)

def draw():
	screen.fill(BLACK)
	all_sprites.draw(screen)
	pygame.display.flip()

while running:
    clock.tick(FPS)
    events()
    threading.Thread(target = update, args = ()).start()
    threading.Thread(target = draw, args = ()).start()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

pygame.quit()

from pygame import *
from settings import *
from moteur import *
import random 
import time 

pygame.init() 
pygame.mixer.init() 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE) 
timer = pygame.time.Clock() 
running = True 

#######################################################################################################################################

def fleche(position1, position2, position3):
    triangle = pygame.draw.polygon(screen, YELLOW,(position1, position2, position3), 6)

bgrd_menu1=pygame.image.load("FOND_menu_play.png")
screen.blit(bgrd_menu1, (0,0))
pygame.display.flip()

bgrdmenu1=pygame.image.load("FOND_perso.png")
screen.blit(bgrdmenu1, (0,0))

menu_entre=True
menu_perso=False
menu_perso_multi=False

pos_fleche_play=((215,200),(280,230),(215,260))
pos_fleche_multi=((215,320),(280,350),(215,380))
pos_fleche_exit=((215,440),(280,470),(215,500))

pos_fleche_p1=((150,190),(240,190),(195,270))
pos_fleche_p2=((740,190),(850,190),(805,270))

choix_entre=1
choix_perso=1

jeu_solo=False
jeu_multi=False
###########################################################################################################################################

fond = pygame.image.load(path.join(path.join(path.dirname(__file__), 'img'), "background.png")).convert() 

class SinglePlayer():
    def __init__(self, skin):
        
        self.playing = True 
        self.player = Player(500, 550, skin, 150)
        self.mob = Mob(WIDTH-50, (HEIGHT/2), "mob.png", 50, self.player) 
        self.final_mob = Mobf(650,100, "final_mob.png", 50, self.player)

        mobs.add(self.mob) 
        mobs.add(self.final_mob)
        all_sprites.add(self.player) 
        all_sprites.add(self.mob) 
        all_sprites.add(self.final_mob)

        self.Levels=["level1.txt"]
        self.world = Level_builder(random.choice(self.Levels), "", "platform.png", "platform.png", "platform.png", "trap.png" )
        self.world.build_level()

        self.TIR_AUTO = pygame.USEREVENT
        pygame.time.set_timer(self.TIR_AUTO, 1000) 



    def events(self):
        
        for event in pygame.event.get(): 

            if self.final_mob : 
                
                if event.type == self.TIR_AUTO:
                    if self.final_mob.life >= 0:
                        self.final_mob.shoot("mob_bullet.png") 

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RIGHT: 
                    self.player.move_d()

                if event.key == pygame.K_LEFT: 
                    self.player.move_g() 

                if event.key == pygame.K_UP: 
                    self.player.jump() 

                if event.key == pygame.K_SPACE: 
                    self.player.shoot("bullet.png") 

            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_RIGHT: 
                    self.player.stop_move_d() 

                if event.key == pygame.K_LEFT: 
                    self.player.stop_move_g()


            if event.type == pygame.QUIT:
                self.playing = False
                running = False 

    def test(self, entity): 

        if entity.rect.top <= HEIGHT / 4:
        
            entity.pos.y += abs(entity.vel.y)
            for plat in platforms: 
                plat.rect.y += abs(entity.vel.y) 
                if plat.rect.top >= HEIGHT:
                
                    plat.kill() 

            for wall in walls: 
                wall.rect.y += abs(entity.vel.y) 
                if wall.rect.top >= HEIGHT:
                    wall.kill() 

            for trap in traps: 
                trap.rect.y += abs(entity.vel.y) 
                if trap.rect.top >= HEIGHT:
                    trap.kill() 
            

        if entity.rect.bottom > HEIGHT: 
            for sprite in all_sprites: 
                sprite.rect.y -= max(entity.vel.y, 10) 
                if sprite.rect.bottom < 0:  
                    sprite.kill()

        if self.player.life <= 0:
            self.playing = False 
                    
        if len(platforms) == 0: 
            self.playing = False 
       
    def update(self): 
        all_sprites.update()

        colision_plat(self.player)
        colision_plat(self.mob) 
        colision_plat(self.final_mob) 
        colision_wall(self.player)  
        colision_wall(self.mob) 
        colision_wall(self.final_mob)

        damage_bullets(self.player)  
        damage_bullets(self.mob) 
        damage_bullets(self.final_mob) 
        damage_mobs(self.player)  
        damage_traps(self.player) 
        
        self.test(self.player)

class Multiplayer():
    def __init__(self, skin_p1, skin_p2):
        
        self.playing = True 
        self.player = Player(WIDTH/4, HEIGHT, skin_p1, 150)
        self.player2 = Player((WIDTH/4)*3, (HEIGHT/2), skin_p2, 150)

        all_sprites.add(self.player)
        all_sprites.add(self.player2) 

        self.Levels=["level1.txt"]
        self.world = Level_builder(random.choice(self.Levels), "", "platform.png", "platform.png", "platform.png", "trap.png" )
        self.world.build_level()



    def events(self):
        
        for event in pygame.event.get(): 

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_RIGHT: 
                    self.player.move_d()

                if event.key == pygame.K_LEFT: 
                    self.player.move_g() 

                if event.key == pygame.K_UP: 
                    self.player.jump() 

                if event.key == pygame.K_SPACE: 
                    self.player.shoot("bullet.png") 

            if event.type == pygame.KEYUP: 
                if event.key == pygame.K_RIGHT: 
                    self.player.stop_move_d() 

                if event.key == pygame.K_LEFT: 
                    self.player.stop_move_g()

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_d: 
                    self.player2.move_d() 

                if event.key == pygame.K_a: 
                    self.player2.move_g()

                if event.key == pygame.K_w:
                    self.player2.jump() 

                if event.key == pygame.K_k: 
                    self.player2.shoot("bullet.png") 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d: 
                    self.player2.stop_move_d() 
                if event.key == pygame.K_a: 
                    self.player2.stop_move_g() 


            if event.type == pygame.QUIT:
                self.playing = False
                running = False 

    def test(self, entity): 

        if entity.rect.top <= HEIGHT / 4:
        
            entity.pos.y += abs(entity.vel.y)
            for plat in platforms: 
                plat.rect.y += abs(entity.vel.y) 
                if plat.rect.top >= HEIGHT:
                
                    plat.kill() 

            for wall in walls: 
                wall.rect.y += abs(entity.vel.y) 
                if wall.rect.top >= HEIGHT:
                    wall.kill() 

            for trap in traps: 
                trap.rect.y += abs(entity.vel.y) 
                if trap.rect.top >= HEIGHT:
                    trap.kill() 
            

        if entity.rect.bottom > HEIGHT: 
            for sprite in all_sprites: 
                sprite.rect.y -= max(entity.vel.y, 10) 
                if sprite.rect.bottom < 0:  
                    sprite.kill()

        if self.player.life <= 0:
            self.playing = False 
                    
        if len(platforms) == 0: 
            self.playing = False 
       
    
    def update(self): 
        all_sprites.update()

        colision_plat(self.player) 
        colision_wall(self.player)
        colision_plat(self.player2) 
        colision_wall(self.player2)

        damage_bullets(self.player) 
        damage_traps(self.player)
        damage_bullets(self.player2) 
        damage_traps(self.player2)
        
        if self.player.pos.y > self.player2.pos.y :
            self.test(self.player)
        else :
            self.test(self.player2)


def draw(): 
	screen.blit(fond, (0,0)) 
	all_sprites.draw(screen) 
	pygame.display.flip()

##########################################################################################################################################

while running:

    while menu_entre:

        for event in pygame.event.get():

            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    running = False
                    menu_entre=False
                    menu_perso=False

                if event.key==K_DOWN:
                    choix_entre+=1
                    screen.blit(bgrd_menu1, (0,0))
                    if choix_entre==1:
                        fleche((215,200),(280,230),(215,260))
                    if choix_entre==2:
                        fleche((215,320),(280,350),(215,380))
                    if choix_entre==3:
                        fleche((215,440),(280,470),(215,500))
                    if choix_entre==4:
                        choix_entre=1
                        fleche((215,200),(280,230),(215,260))
                    pygame.display.flip()

                if event.key==K_UP:
                    choix_entre-=1
                    screen.blit(bgrd_menu1, (0,0))
                    if choix_entre==1:
                        fleche((215,200),(280,230),(215,260))
                    if choix_entre==2:
                        fleche((215,320),(280,350),(215,380))
                    if choix_entre==3:
                        fleche((215,440),(280,470),(215,500))
                    if choix_entre==0:
                        choix_entre=1
                        fleche((215,200),(280,230),(215,260))
                    pygame.display.flip()

                if event.key==K_RETURN:
                    if choix_entre==1 or choix_entre==4 or choix_entre==0:
                        menu_entre=False
                        menu_perso=True
                        screen.blit(bgrdmenu1, (0,0))
                        pygame.display.flip()

                    if choix_entre==2:
                        menu_entre=False
                        menu_perso_multi=True
                        screen.blit(bgrdmenu1, (0,0))
                        pygame.display.flip()

                    if choix_entre==3:
                        running = False
                        menu_entre=False
                        menu_perso=False


    while menu_perso:

        for event in pygame.event.get():
            
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    menu_entre = True
                    menu_perso=False


                if event.key==K_LEFT:
                    choix_perso-=1
                    screen.blit(bgrdmenu1, (0,0))
                    if choix_perso==1:
                        fleche((150,190),(240,190),(195,270))
                    if choix_perso==2:
                        fleche((740,190),(850,190),(805,270))
                    if choix_perso==0:
                        choix_perso=2
                        fleche((150,190),(240,190),(195,270))
                    pygame.display.flip()

                if event.key==K_RIGHT:
                    choix_perso+=1
                    screen.blit(bgrdmenu1, (0,0))
                    if choix_perso==1:
                        fleche((150,190),(240,190),(195,270))
                    if choix_perso==2:
                        fleche((740,190),(850,190),(805,270))
                    if choix_perso==3:
                        choix_perso=1
                        fleche((150,190),(240,190),(195,270))
                    pygame.display.flip()

                if event.key==K_RETURN:
                    if choix_perso==1 or choix_perso==0 or choix_perso==3:
                        menu_perso=False
                        jeu_solo=True
                        skin="player1.png"

                    if choix_perso==2:
                        menu_perso=False
                        jeu_solo=True
                        skin="player2.png"

    while menu_perso_multi:

        for event in pygame.event.get():
            
            if event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    menu_entre = True
                    menu_perso_multi=False


                if event.key==K_LEFT:
                    choix_perso-=1
                    screen.blit(bgrdmenu1, (0,0))
                    if choix_perso==1:
                        fleche((150,190),(240,190),(195,270))
                    if choix_perso==2:
                        fleche((740,190),(850,190),(805,270))
                    if choix_perso==0:
                        choix_perso=2
                        fleche((150,190),(240,190),(195,270))
                    pygame.display.flip()

                if event.key==K_RIGHT:
                    choix_perso+=1
                    screen.blit(bgrdmenu1, (0,0))
                    if choix_perso==1:
                        fleche((150,190),(240,190),(195,270))
                    if choix_perso==2:
                        fleche((740,190),(850,190),(805,270))
                    if choix_perso==3:
                        choix_perso=1
                        fleche((150,190),(240,190),(195,270))
                    pygame.display.flip()

                if event.key==K_RETURN:
                    if choix_perso==1 or choix_perso==0 or choix_perso==3:
                        menu_perso_multi=False
                        jeu_multi=True
                        skin_p1="player1.png"
                        skin_p2="player2.png"

                    if choix_perso==2:
                        menu_perso_multi=False
                        jeu_multi=True
                        skin_p1="player2.png"
                        skin_p2="player1.png"
                        

    while jeu_solo:
        timer.tick(FPS)
        game = SinglePlayer(skin)
    
        while game.playing:
            game.events()
            game.update()
            draw()

            jeu_multi = game.playing

    while jeu_multi:
        timer.tick(FPS)
        game = Multiplayer(skin_p1, skin_p2)
    
        while game.playing:
            game.events()
            game.update()
            draw()

            jeu_multi = game.playing


pygame.quit()
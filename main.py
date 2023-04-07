#this is our main file for hte game.  here we will import what we need.
import os
import random
import math
import pygame
from os import listdir
from os.path import isfile,join
# import PlayerInfo
# import PlayerMove
# import SpriteLoad

#init pygame
pygame.init()
pygame.display.set_caption("My Platformer")
BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 1000,800
FPS =60

window = pygame.display.set_mode((WIDTH,HEIGHT))

#sprite load class
class SpriteLoad():
    def __init__(self):
        # return self.loadspriteSheets(dir, dir2,width,height)
        pass

    def flip(sprites):
        return [pygame.transform.flip(sprite,True,False) for sprite in sprites]

    def loadspriteSheets(dir, dir2,width,height,direction=False):
        path = join("assets",dir, dir2)
        images = [f for f in listdir(path)  if isfile(join(path,f)) ]
        all_sprites = {}

        for image in images:
            sprite_sheet = pygame.image.load(join(path,image)).convert_alpha()
            sprites = []

            for i in range(sprite_sheet.get_width() //width):
                surface = pygame.surface.Surface((width,height),pygame.SRCALPHA,32)
                rect = pygame.Rect(i*width,0,width, height)
                surface.blit(sprite_sheet,(0,0),rect)
                sprites.append(pygame.transform.scale2x(surface))
            
            if direction:
                all_sprites[image.replace(".png","")+"_right"] = sprites
                all_sprites[image.replace(".png","")+"_left"]= flip(sprites)
            else: 
                all_sprites[image.replace(".png","")]=sprites
        
        return all_sprites
#end of sprite load class



# playerinfo class
class Player(pygame.sprite.Sprite):
    COLOR = (255,255,255)
    GRAVITY = 1
    SpriteLoad()
    SPRITES = SpriteLoad.loadspriteSheets("MainCharacters","MaskDude",32,32)
 
    def __init__(self, x, y, width,height):
        #lets init our player character
        self.rect = pygame.Rect(x,y, width,height)
        self.x_vel = 0
        self.fallcount = 1
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.dest = (x,y)

    def move(self,dx,dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self,vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count =0

    def move_right(self,vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count =0

    def move_up(self,vel):
        self.y_vel = -vel
        if self.direction != "up":
            self.direction = "up"
            self.animation_count =0

    def move_down(self,vel):
        self.y_vel = vel
        if self.direction != "down":
            self.direction = "down"
            self.animation_count =0

    def loop(self,fps):
        #self.y_vel  += min(1,(self.fallcount/fps)*self.GRAVITY)
        self.move(self.x_vel,self.y_vel)
        self.fallcount = self.fallcount+1

    def draw(self, win):

        pygame.draw.rect(win,self.COLOR,self.rect)
        self.sprite = self.SPRITES["idle"][0] 
        win.blit(self.sprite,self.dest)
# End of player info


# player move class
PLAYER_VEL = 5

class PlayerMove():
    def __init__(self) -> None:
        pass


    def handle_move(self,player):
        # player.x_vel = 0
        # player.y_vel = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left(PLAYER_VEL)
        if keys[pygame.K_RIGHT]:
            player.move_right(PLAYER_VEL)
        # if keys[pygame.K_UP]:
        #     player.move_up(PLAYER_VEL)            
        # if keys[pygame.K_DOWN]:
        #     player.move_down(PLAYER_VEL)            

#end of player move class



#  this is the generic methods, not linked to any classes. Considered main
def get_background(name):
    #this method will go through and generate the back ground for game

    image = pygame.image.load(join("assets","Background",name))
    _,_,width,height = image.get_rect()

    tiles =[]
    for x in range(WIDTH//width+1):
        for y in range(HEIGHT // height +1):
            pos = (x*width,y*height)
            tiles.append(pos)

    return tiles, image


def draw(window, background,bg_image,player):
    #this method will draw out the game window
    for tile in background:
        window.blit(bg_image,tile)
    
    player.draw(window)
    pygame.display.update()

def main(window):
    #our main function which will be our entry point
    clock = pygame.time.Clock()
    pygame.init()
    background, bg_image = get_background("Blue.png")

    player = Player(100,100,50,50)
    playerMover = PlayerMove()
    sprite_loader = SpriteLoad()

    run = True
    while run:
        clock.tick(FPS)
        #this will get our events for the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        player.loop(FPS)
        playerMover.handle_move(player)
        draw(window,background,bg_image,player)


    #lets leave the game
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
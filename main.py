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
def flip_it(sprites):
        return [pygame.transform.flip(sprite,True,False) for sprite in sprites]

def get_block(size):
    path = join("assets","Terrain","Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size),pygame.SRCALPHA,32)
    rect = pygame.Rect(96,0,size, size)
    surface.blit(image,(0,0),rect)
    return pygame.transform.scale2x(surface)

class Object(pygame.sprite.Sprite):
    def __init__(self, x,y,width, height, name = None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width,height),pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self,win,offset_x):
        win.blit(self.image,(self.rect.x-offset_x,self.rect.y))

class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size,size )
        block = get_block(size)
        self.image.blit(block,(0,0))
        self.mask = pygame.mask.from_surface(self.image)

class SpriteLoad():
    def __init__(self):
        # return self.loadspriteSheets(dir, dir2,width,height)
        pass

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
                all_sprites[image.replace(".png","")+"_left"] = flip_it(sprites)
            else: 
                all_sprites[image.replace(".png","")]=sprites
        
        return all_sprites
#end of sprite load class



# playerinfo class
class Player(pygame.sprite.Sprite):
    COLOR = (255,255,255)
    GRAVITY = 1
    SpriteLoad()
    SPRITES = SpriteLoad.loadspriteSheets("MainCharacters","MaskDude",32,32,True)
    ANIMATION_DELAY = 2
 
    def __init__(self, x, y, width,height):
        #lets init our player character
        super().__init__()

        self.rect = pygame.Rect(x,y, width,height)
        self.x_vel = 0
        self.fallcount = 1
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.dest = (x,y)
        self.IsLanded = False
        self.jump_count =0 

    def jump(self):
        self.y_vel = -self.GRAVITY * 16
        self.animation_count =0 
        self.jump_count +=1
        if self.jump_count==1:
            self.fall_count  =0

 

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0 
        self.jump_count =0 
 
    def hit_head(self):
        self.count =0
        self.y_vel =-1*self.y_vel


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
        # if self.IsLanded == False:
        self.y_vel  += min(1,(self.fallcount/fps)*self.GRAVITY)
        self.move(self.x_vel,self.y_vel)
        self.fallcount = self.fallcount+1

        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.x_vel!=0:
            sprite_sheet = "run"
        if self.y_vel<0:
            if self.jump_count==1:
                sprite_sheet="jump"
            elif self.jump_count==2:
                sprite_sheet="double_jump"
        elif self.y_vel >self.GRAVITY*2:
            sprite_sheet = "fall"

        sprite_sheet_name = sprite_sheet + "_"+self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count//self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count +=1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win,offset_x):
        # pygame.draw.rect(win,self.COLOR,self.rect)
        # win.blit(self.sprite,self.dest)
        # self.sprite = self.SPRITES["idle_"+self.direction][0] 

        win.blit(self.sprite,(self.rect.x-offset_x,self.rect.y) )


# End of player info


# player move class
PLAYER_VEL = 5
def handle_vertical_collision(player,objects,dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            if dy>0:
                player.rect.bottom = obj.rect.top
                player.landed()
            if dy<0:
                player.rect.top = obj.rect.bottom
                player.hit_head()
        collided_objects.append(obj)
    return collided_objects

def collide_left(player,objects,dx):
    colided_object = []
    player.move(dx, 0)
    player.update()
    blocknotground = False


    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            y = obj.rect.centery
            blocknotground  = y <700
            colided_object.append(obj)
            
    if blocknotground==False:
        colided_object.clear()
    player.move(-dx, 0)
    player.update()

    return colided_object

def collide_right(player,objects,dx):
    colided_object = []
    player.move(dx, 0)
    player.update()
    blocknotground = False


    for obj in objects:
        if pygame.sprite.collide_mask(player,obj):
            y = obj.rect.centery
            blocknotground  = y <700 and player.rect.centerx < obj.rect.centerx
            colided_object.append(obj)
            
    if blocknotground==False:
        colided_object.clear()
    player.move(-dx, 0)
    player.update()

    return colided_object


class PlayerMove():
    def __init__(self) -> None:
        pass

    def handle_move(self,player,objects):
        player.x_vel = 0
        # colide_left = False
        # colide_right = False

        colide_left = collide_left(player,objects,-PLAYER_VEL*2)
        colide_right = collide_right(player,objects,PLAYER_VEL*2)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and len(colide_left) <=1 :
            player.move_left(PLAYER_VEL)
        if keys[pygame.K_RIGHT] and len(colide_right) <=1:
            player.move_right(PLAYER_VEL)
 
        handle_vertical_collision(player,objects,player.y_vel)

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


def draw(window, background,bg_image,player,objects,offset_x):
    #this method will draw out the game window
    for tile in background:
        window.blit(bg_image,tile)

    for obj in objects:
        obj.draw(window,offset_x)

    player.draw(window,offset_x)
    pygame.display.update()




def main(window):
    #our main function which will be our entry point
    clock = pygame.time.Clock()
    pygame.init()
    background, bg_image = get_background("Blue.png")

    offset_x =0
    scroll_area_width = 200
    player = Player(100,100,50,50)
    block_size = 96
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)  for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size), Block(block_size * 3, HEIGHT - block_size * 4, block_size)]

    itemtodraw = objects

   # blocks =[Block(0,HEIGHT-block_size,block_size)]
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
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and player.jump_count<2:
                    player.jump()

        player.loop(FPS)
        playerMover.handle_move(player,itemtodraw)
        draw(window,background,bg_image,player,itemtodraw,offset_x)
        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

    #lets leave the game
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
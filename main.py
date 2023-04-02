#this is our main file for hte game.  here we will import what we need.
import os
import random
import math
import pygame
from os import listdir
from os.path import isfile,join


#init pygame
pygame.init()
pygame.display.set_caption("My Platformer")
BG_COLOR = (255,255,255)
WIDTH, HEIGHT = 1000,800
FPS =60
PLAYER_VEL = 5

window = pygame.display.set_mode((WIDTH,HEIGHT))

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


def draw(window, background,bg_image):
    #this method will draw out the game window
    for tile in background:
        window.blit(bg_image,tile)
    
    pygame.display.update()

def main(window):
    #our main function which will be our entry point
    clock = pygame.time.Clock()
    
    background, bg_image = get_background("Blue.png")



    run = True
    while run:
        clock.tick(FPS)
        #this will get our events for the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(window,background,bg_image)


    #lets leave the game
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)
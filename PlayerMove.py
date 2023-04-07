#this class will hold all the player infor we need.
import os
import random
import math
import PlayerInfo
import pygame
from os import listdir
from os.path import isfile,join


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
#this class will hold all the player infor we need.
import os
import random
import math
import pygame
import  SpriteLoad

from os import listdir
from os.path import isfile,join

class Player(pygame.sprite.Sprite):
    COLOR = (255,255,255)
    GRAVITY = 1
    SPRITES = SpriteLoad.SpriteLoad("MainCharacters","MaskDude",32,32)
 
    def __init__(self, x, y, width,height):
        #lets init our player character
        self.rect = pygame.Rect(x,y, width,height)
        self.x_vel = 0
        self.fallcount = 1
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0

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
        win.blit(self.sprite)

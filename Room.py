import pygame
from collections import deque
from random import randint
from Tile import *

class Room(object):
    def __init__(self, game, base, door, background, full_background, props, enemies):
        self.base = base
        self.door = door #list of doors that this room has
        self.game = game 

        self.background = background #filename of the background image for this room's tiles

        self.full_background = full_background

        self.full_background_image = pygame.image.load(self.full_background).convert_alpha()

        self.doors = door

        rows, cols = (8, 8)

        self.props = props

        self.enemies = enemies

        #initialize array the manual way
        self.tiles = [[0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0]]

        

        x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for x in range(0, 8):
            for y in range(0, 8):
                self.tiles[x][y] = Tile(self.game, x1[x], x1[y], background) #fill the 2d array with tile objects 
        

import pygame
from collections import deque
from random import randint

class Tile(pygame.sprite.Sprite): #create class for the tile (child class of pygame.sprite.Sprite
    def __init__(self, game, x, y, background):
        self.groups = game.all_sprites, game.all_tiles #set this sprite's groups to
        #the all_sprites and tiles groups created in the main file's main method.
        pygame.sprite.Sprite.__init__(self, self.groups)#call parent class constructor
        self.game = game

        #all images in pygame are called "surfaces"
        #self.image = pygame.Surface((64, 64))

        self.image = pygame.image.load(background).convert()

        #self.image.fill((0, 255, 0)) #make each tile green (for now)

        self.rect = self.image.get_rect() #get rectangular area of the surface

        self.x = x

        self.y = y

        self.rect.x = x * 64

        self.rect.y = y * 64

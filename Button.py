import pygame
from collections import deque
from random import randint

class Button(pygame.sprite.Sprite): #define button class for the inventory GUI
    def __init__(self, game, x, y, functionality, image, xOffset, yOffset):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.x = x

        self.y = y

        self.functionality = functionality #variable to describe what the button does

        self.image = pygame.image.load(image).convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x + xOffset

        self.rect.y = y + yOffset

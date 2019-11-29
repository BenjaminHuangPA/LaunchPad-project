import pygame
from collections import deque
from random import randint

class Prop(pygame.sprite.Sprite): #props are just background images, like tables or chairs
    def __init__(self, x, y, name, value, isInteractable, spriteImage):

        #self.game = game

        #self.groups = game.props

        pygame.sprite.Sprite.__init__(self)

        #self.game = game

        self.x = x

        self.y = y

        self.image = pygame.image.load(spriteImage).convert_alpha()

        self.rect = self.image.get_rect()

        self.name = name

        self.value = value

        self.isInteractable = isInteractable

        self.rect.x = x

        self.rect.y = y

import pygame
from collections import deque
from random import randint

class item(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, name, value, description, isConsumable, rarity, ID):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game

        self.x = x

        self.y = y

        self.type = "item"

        self.image = pygame.image.load(image).convert()

        self.name = name

        self.value = value

        self.description = description

        self.isConsumable = isConsumable

        self.rarity = rarity

        self.ID = ID

        self.rect = self.image.get_rect()

        self.rect.x = x

        self.rect.y = y

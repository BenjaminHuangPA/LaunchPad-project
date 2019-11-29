import pygame
from collections import deque
from random import randint
from Enemy import *

class enemyStatusBar(pygame.sprite.Sprite):
    def __init__(self, game, enemy, x, y):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.enemy = enemy

        self.x = x

        self.y = y

        self.image = pygame.image.load("img/menu/enemy_status_bar.png").convert_alpha()

       

        self.portrait = pygame.image.load("img/enemy/goblin/portrait.png").convert_alpha()

        self.image.blit(self.portrait, (16, 19))

        self.rect = self.image.get_rect()

        self.rect.x = x

        self.rect.y = y

        self.initializeHealthBar()

        self.initializeText()

    def initializeHealthBar(self):
        healthBarLength = self.enemy.HP * 3
        healthBarRect = pygame.Rect(176, 62, healthBarLength, 11)
        pygame.draw.rect(self.image, (141, 42, 42), healthBarRect)

    def increaseHealth(self, health):
        print(self.enemy.HP)
        if(self.enemy.HP < self.enemy.maxHP):
            newHealth = pygame.Rect(176, 62, 3 * self.enemy.HP, 11)
            pygame.draw.rect(self.image, (141, 42, 42), newHealth)
        else:
            fullHP = pygame.Rect(176, 62, 3 * self.enemy.maxHP, 11)
            pygame.draw.rect(self.image, (141, 42, 42), fullHP)
            

    def decreaseHealth(self):
        print(self.enemy.HP)
        if(self.enemy.HP > 0):
            remainingHP = (self.enemy.HP) * 3
            maxHP = (self.enemy.maxHP - self.enemy.HP) * 3
            healthLost = pygame.Rect(176 + remainingHP, 62, maxHP, 11)
            pygame.draw.rect(self.image, (82, 51, 46), healthLost)
        else:
            noHP = pygame.Rect(176, 62, self.enemy.maxHP * 3, 11)
            pygame.draw.rect(self.image, (82, 51, 46), noHP)

    def initializeText(self):
        pygame.font.init()
        name = self.enemy.name

        classification = self.enemy.classification

        nameFont = pygame.font.SysFont("Times New Roman", 25)

        nameText = nameFont.render(name, False, (255, 255, 255))

        self.image.blit(nameText, (110, 7))

        classFont = pygame.font.SysFont("Times New Roman", 16)

        classText = classFont.render(classification, False, (255, 255, 255))

        self.image.blit(classText, (110, 33))

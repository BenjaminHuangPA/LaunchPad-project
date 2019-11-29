import pygame
from collections import deque
from random import randint

class Door(pygame.sprite.Sprite):
    def __init__ (self, game, x, y, orientation, status, spriteImage, bgImage):
        self.groups = game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.spriteImage = spriteImage

        self.bgImage = bgImage #get the background wall's image so we can blit over the open doors once they're no longer open

        self.image = pygame.image.load(spriteImage).convert()

        self.rect = self.image.get_rect()

        self.x = x

        self.y = y

        self.orientation = orientation #denotes if the door is "forward", "backward", "left", or "right"

        self.status = status #denotes if the door is open or closed (True is open, False is closed)

        #self.image = spriteImage

        if self.status == False:
            self.image = pygame.image.load("door_blocked.png").convert()

        self.rect.x = x * 64

        self.rect.y = y * 64

    #these two methods change the door's appearance to show that it's shut or open

    def closeDoor(self):
        bgWall = pygame.image.load(self.bgImage).convert()
        print(self.x)
        print(self.y)
        if self.orientation == "right":
            self.image.blit(bgWall, (0, 0), (0, self.y * 64, 64, 64))
        elif self.orientation == "left":
            self.image.blit(bgWall, (0, 0), (0, self.y * 64, 64, 64))
        elif self.orientation == "forward":
            self.image.blit(bgWall, (0, 0), (self.x * 64, 0, 64, 64))
        elif self.orientation == "backward":
            self.image.blit(bgWall, (0, 0), (self.x * 64, 0, 64, 64))

    def openDoor(self):
        self.image = pygame.image.load(self.spriteImage).convert()

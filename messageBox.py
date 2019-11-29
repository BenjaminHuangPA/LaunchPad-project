import pygame
from collections import deque
from random import randint
from Player import *

class messageBox(pygame.sprite.Sprite): #simple class for displayed closeable messages to the player
    def __init__(self, game, player, x, y, message):


        self.groups = game.active_message_boxes

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.game.message_box_active = True

        self.player = player

        self.x = x

        self.y = y

        self.message = message

        self.image = pygame.image.load("img/menu/message_box.png").convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x * 1

        self.rect.y = y * 1

        self.okButton = Button(self.game, 141, 113, "OK", "img/menu/ok_button.png", 64, 128)

        self.image.blit(self.okButton.image, (self.okButton.x, self.okButton.y))

        textwrapper = textWrapper()

        textwrapper.blitText(self.image, 58, 28, message, 296, 22, 20, (255, 255, 255))
  

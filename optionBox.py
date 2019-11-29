import pygame
from collections import deque
from random import randint
from Player import *

class optionBox(pygame.sprite.Sprite):
    def __init__(self, game, x, y, player, messages, mainMessage):
        self.groups = game.active_option_boxes

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.player = player

        self.messages = messages

        self.mainMessage = mainMessage

        self.x = x

        self.y = y

        self.messages = messages

        self.image = pygame.image.load("img/menu/dialog_box.png").convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x

        self.rect.y = y

        self.buttons = []
        
        self.initialize()
        

    def initialize(self):

        pygame.font.init()

        textwrapper = textWrapper()

        
        if self.messages[1] == None and self.messages[2] == None and self.messages[3] == None: #only one choice
            self.button1 = Button(self.game, 219, 76, "Message 1", "img/menu/blank_button.png", 0, 0)
            self.buttons = [self.button1]
             
        elif self.messages[2] == None and self.messages[3] == None: #two choices
            self.button1 = Button(self.game, 158, 77, "Message 1", "img/menu/blank_button.png", 0, 0)
            self.button2 = Button(self.game, 280, 77, "Message 2", "img/menu/blank_button.png", 0, 0)
            self.buttons = [self.button1, self.button2]
            
        elif self.messages[3] == None:
            self.button1 = Button(self.game, 97, 77, "Message 1", "img/menu/blank_button.png", 0, 0)
            self.button2 = Button(self.game, 219, 77, "Message 2", "img/menu/blank_button.png", 0, 0)
            self.button3 = Button(self.game, 341, 77, "Message 3", "img/menu/blank_button.png", 0, 0)
            self.buttons = [self.button1, self.button2, self.button3]
            
        else:
            self.button1 = Button(self.game, 73, 77, "Message 1", "img/menu/blank_button.png", 0, 0)
            self.button2 = Button(self.game, 171, 77, "Message 2", "img/menu/blank_button.png", 0, 0)
            self.button3 = Button(self.game, 269, 77, "Message 3", "img/menu/blank_button.png", 0, 0)
            self.button4 = Button(self.game, 367, 77, "Message 4", "img/menu/blank_button.png", 0, 0)
            self.buttons = [self.button1, self.button2, self.button3, self.button4]
            
        counter = 0
        for button in self.buttons:
            textwrapper.blitText(button.image, 6, 3, self.messages[counter], 60, 15, 1, (255, 255, 255))
            self.image.blit(button.image, (button.x, button.y))
            counter += 1
        
        main_font = pygame.font.SysFont("Times New Roman", 15)
        main_message_text = main_font.render(self.mainMessage, False, (255, 255, 255))
        self.image.blit(main_message_text, (46, 30))

    def checkClicked(self, x, y):
        offsetX = x - self.x
        offsetY = y - self.y
        print(offsetX)
        print(offsetY)
        for button in self.buttons:
            print(button.rect)
            if button.rect.collidepoint(offsetX, offsetY) == True:
                print("True")
                return(self.buttons.index(button) + 1)

    #def functions(self, function, *args):
    #    if function == "Pick up":
            
            

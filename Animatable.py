import pygame
from collections import deque
from random import randint
from Prop import *
from spriteSheet import *

class Animatable(Prop): #this subclass of prop is for things that are animated. 
    def __init__(self, x, y, game, name, value, isInteractable, spriteImage, spriteSheetName, rows, cols, animDelay, bg, isRepeating, bgImageSource):

        super().__init__(x, y, name, value, isInteractable, spriteImage) #call prop's constructor 

        self.game = game

        self.spriteSheetName = spriteSheetName #spriteSheetName is the image directory of the sprite sheet image

        self.animDelay = animDelay #To be implemented: an animation delay so that the animation is'nt being played at 30 fps (at game speed)

        self.animation = spriteSheet(spriteSheetName, rows, cols) #make an instance of class spriteSheet (See above)

        self.animationList = self.animation.getSpriteList(); #get a list of tuples representing the upper left corners of individual frames in the sprite sheet

        self.animationCount = 1 #initialize the index of animation to 0

        if bgImageSource == None:
            self.bgImage = pygame.image.load(bg).convert_alpha() #load the background image
        else:
            self.bgImage = bgImageSource

        self.isRepeating = isRepeating
        
        self.add(game.all_sprites)

    def animate(self):
        if self.animationCount < len(self.animationList):
            spriteTuple = self.animationList[self.animationCount]
            self.replaceBackground()
            self.animation.draw(self.image, spriteTuple[0], spriteTuple[1])
           
            if self.animationCount == len(self.animationList) - 1:
                if self.isRepeating == True:
                    self.animationCount = 0
                else:
                    self.animationCount == len(self.animationList)
                    #self.replaceBackground()
            else:
                self.animationCount += 1

    def permaErase(self):
        self.animationCount = len(self.animationList)
        self.replaceBackground()

    def replaceBackground(self):
        
        #self.image.blit(self.bgImage, (0, 0), (64, 64, 64, 64))
        self.image.blit(self.bgImage, (0, 0))

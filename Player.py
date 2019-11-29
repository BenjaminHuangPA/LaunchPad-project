import pygame
from collections import deque
from random import randint
from spriteSheet import *

class Player(pygame.sprite.Sprite):
    
    def __init__(self, game, x, y, inventory, HP, maxHP, STM, maxSTM, STR, AGL, INT, DEX, GRD, headArmor, torsoArmor, armArmor, legArmor, lWeapon, rWeapon):
        self.groups = game.all_sprites, game.entities #set the player's sprite group to all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.name = "Horace"

        self.current_zone = 1

        self.roomLocation = [5, 1] #denote where in the gameloop's 2d zone array the player is. i.e. index 1 of array 5.

        self.image = pygame.image.load("img/misc/test.png").convert_alpha() #.convert_alpha() enables png transparency

        self.rect = self.image.get_rect() #how pygame knows where to draw the sprite (VERY IMPORTANT)
        #get rect returns the size of the sprite's image

        self.x = x

        self.y = y

        #note: pygame relies on three attributes to know where to draw sprites: the sprite's self.x, self.y and self.rect

        self.forward = False

        self.backward = False

        self.left = False

        self.right = False

        #self.speed = 10

        self.playerWalkLeft = spriteSheet("img/horace/horace_walk_left.png", 8, 1) #initialize spriteSheet object for the player walking to the left

        self.playerWalkLeftList = self.playerWalkLeft.getSpriteList() #get list of coordinates representing the upper left corners of the individiual sprites in the spriteSheet

        self.walkLeftCount = 0 

        self.playerWalkRight = spriteSheet("img/horace/horace_walk_right.png", 8, 1) #initialize spriteSheet object for the player walking to the right

        self.playerWalkRightList = self.playerWalkRight.getSpriteList()

        self.walkRightCount = 0 

        self.playerWalkForward = spriteSheet("img/horace/horace_walk_back.png", 6, 1)

        self.playerWalkForwardList = self.playerWalkForward.getSpriteList() #initialize spriteSheet object for the player walking forward

        self.walkForwardCount = 0

        self.playerWalkBackward = spriteSheet("img/horace/horace_walk_front.png", 6, 1)

        self.playerWalkBackwardList = self.playerWalkBackward.getSpriteList() #initialize spriteSheet object for the player walking backwards

        self.walkBackwardCount = 0

        self.inventory = inventory #inventory instance variable

        self.HP = HP

        self.maxHP = maxHP

        self.STM = STM

        self.maxSTM = STM

        self.STR = STR

        self.AGL = AGL

        self.INT = INT

        self.DEX = DEX

        self.GRD = GRD

        self.headArmor = headArmor

        self.torsoArmor = torsoArmor

        self.armArmor = armArmor

        self.legArmor = legArmor

        self.lWeapon = lWeapon

        self.rWeapon = rWeapon

        self.background = pygame.image.load("img/tile/chasm/chasm_01_full.png").convert() #load full background image

        self.targetableAreas = ["Target: head", "Target: arms", "Target: legs", "Target: torso"]

        self.learnedMoves = {"Swing": self.randKeys(3), "Thrust": self.randKeys(5), "Lunge": self.randKeys(6)} 

    def randKeys(self, keys):
        combo = ""
        for i in range(0, keys):
            random_integer = randint(1, 4)
            if random_integer == 1:
                combo = combo + "LEFT"
            elif random_integer == 2:
                combo = combo + "RIGHT"
            elif random_integer == 3:
                combo = combo + "UP"
            elif random_integer == 4:
                combo = combo + "DOWN"
	    
            if i < keys - 1:
                combo = combo + " "
        return(combo)

    def move(self, x, y):
        
        #if(self.checkWallCollision() == True):
        self.walkAnim(x, y) #play the walking animation (See below)
        self.x += x #move player left/right
        self.y += y #move player right/left
        

    def randKeys(self, keys):
        combo = ""
        for i in range(0, keys):
            random_integer = randint(1, 4)
            if random_integer == 1:
                combo = combo + "LEFT"
            elif random_integer == 2:
                combo = combo + "RIGHT"
            elif random_integer == 3:
                combo = combo + "UP"
            elif random_integer == 4:
                combo = combo + "DOWN"
            if i < keys:
                combo = combo + " "
        return(combo)


    def takeDamage(self, DMG):
        self.HP = self.HP - DMG


    def heal(self, HP):
        self.HP = self.HP + HP

    def canEquip(self, item):
        flag = True
        if item.statReq["STR"] > self.STR:
            flag = "strength"
        if item.statReq["DEX"] > self.DEX:
            flag = "dexterity"
        if item.statReq["AGL"] > self.AGL:
            flag = "agility"
        if item.statReq["INT"] > self.INT:
            flag = "intelligence"
        if(flag == True):
            print("all good!")
        
        return flag
        
    
        
    def equipArmor(self, armor):
        if armor.region == "head":
            self.headArmor = armor
        elif armor.region == "torso":
            self.torsoArmor = armor
        elif armor.region == "arms":
            self.armArmor = armor
        elif armor.region == "legs":
            self.legArmor = armor
        self.game.callUpdateStatusBar(0)

    def equipWeapon(self, weapon):
        if weapon.hand == "left":
            self.lWeapon = weapon
        elif weapon.hand == "right":
            self.rWeapon = weapon
            

    def unequipArmor(self, region):
        if region == "head":
            self.headArmor = None
        elif region == "torso":
            self.torsoArmor = None
        elif region == "arms":
            self.armArmor = None
        elif region == "legs":
            self.legArmor = None
        self.game.callUpdateStatusBar(0)


    def unequipWeapon(self, hand):
        if hand == "lweapon":
            self.lWeapon = None
        elif hand == "rweapon":
            self.rWeapon = None

    def getElemDef(self):
        
        light = 0
        dark = 0
        fire = 0
        ice = 0

        armors = [self.headArmor, self.torsoArmor, self.armArmor, self.legArmor]

        for armor in armors:
            if armor != None:
                print(armor.name)
                light += armor.elemBonus["LIGHT"]
                dark += armor.elemBonus["DARK"]
                fire += armor.elemBonus["FIRE"]
                ice += armor.elemBonus["ICE"]
            else:
                continue

        elemDefArray = [light, dark, fire, ice]

        return elemDefArray

    

    def getElemATTKLeft(self):
        if self.lWeapon == None:
            empty = [0, 0, 0, 0]
            return empty
        else:
            light = self.lWeapon.elemBonus["LIGHT"]
            dark = self.lWeapon.elemBonus["DARK"]
            fire = self.lWeapon.elemBonus["FIRE"]
            ice = self.lWeapon.elemBonus["ICE"]
            elemATTKLeftArray = [light, dark, fire, ice]
            return elemATTKLeftArray

    def getElemATTKRight(self):
        if self.rWeapon == None:
            empty = [0, 0, 0, 0]
            return empty
        else:
            light = self.rWeapon.elemBonus["LIGHT"]
            dark = self.rWeapon.elemBonus["DARK"]
            fire = self.rWeapon.elemBonus["FIRE"]
            ice = self.rWeapon.elemBonus["ICE"]
            elemATTKRightArray = [light, dark, fire, ice]
            return elemATTKRightArray
        
        
    def walkAnim(self, x, y):
        if x < 0: #if the player walks to the left (change in x pos less than 0)
            self.left = True
            
            
            if self.walkLeftCount < len(self.playerWalkLeftList): #loop through the list of sprites of the player walking
                leftSpriteTuple = self.playerWalkLeftList[self.walkLeftCount] #
                self.replaceBackground("left") #call blitOut2 method to blit new blank background onto the image
                self.playerWalkLeft.draw(self.image, leftSpriteTuple[0], leftSpriteTuple[1]) #call the sprite class instance's draw method to blit the correct sprite onto the image
                self.renderEquipment("left", leftSpriteTuple[0], leftSpriteTuple[1])
                if self.walkLeftCount == len(self.playerWalkLeftList) - 1: 
                    self.walkLeftCount = 0 #if reached the end of the array of sprites, start over at the beginning
                else:
                    self.walkLeftCount += 1 #else, go to the next sprite
        
        if x > 0: #handle walking right
            
            self.right = True
            
            
            if self.walkRightCount < len(self.playerWalkRightList):
                rightSpriteTuple = self.playerWalkRightList[self.walkRightCount]
                self.replaceBackground("right")
                self.playerWalkRight.draw(self.image, rightSpriteTuple[0], rightSpriteTuple[1])
                self.renderEquipment("right", rightSpriteTuple[0], rightSpriteTuple[1])
                if self.walkRightCount == len(self.playerWalkRightList) - 1:
                    self.walkRightCount = 0
                else:
                    
                    self.walkRightCount += 1
        if y > 0: #walking "backward"

            self.backward = True
            
            if self.walkBackwardCount < len(self.playerWalkBackwardList):
                downSpriteTuple = self.playerWalkBackwardList[self.walkBackwardCount]
                self.replaceBackground("down")
                self.playerWalkBackward.draw(self.image, downSpriteTuple[0], downSpriteTuple[1])
                self.renderEquipment("down", downSpriteTuple[0], downSpriteTuple[1])
                if self.walkBackwardCount == len(self.playerWalkBackwardList) - 1:
                    self.walkBackwardCount = 0
                else:
                    self.walkBackwardCount += 1
        if y < 0: #walking "forward"

            self.forward = True
            
            if self.walkForwardCount < len(self.playerWalkForwardList):
                upSpriteTuple = self.playerWalkForwardList[self.walkForwardCount]
                self.replaceBackground("up")
                self.playerWalkForward.draw(self.image, upSpriteTuple[0], upSpriteTuple[1])
                self.renderEquipment("up", upSpriteTuple[0], upSpriteTuple[1])
                if self.walkForwardCount == len(self.playerWalkForwardList) - 1:
                    self.walkForwardCount = 0
                else:
                    self.walkForwardCount += 1
        #pygame.display.update()

    def idle(self):
        
        if self.forward == True:
            self.replaceBackground("up")
            self.playerWalkForward.draw(self.image, 0, 0)
            self.renderEquipment("up", 0, 0)
            self.forward = False
        elif self.backward == True:
            self.replaceBackground("down")
            self.playerWalkBackward.draw(self.image, 0, 0)
            self.renderEquipment("down", 0, 0)
            self.backward = False
        elif self.left == True:
            self.replaceBackground("left")
            self.playerWalkLeft.draw(self.image, 0, 0)
            self.renderEquipment("left", 0, 0)
            self.left = False
        else:
            self.replaceBackground("right")
            self.playerWalkRight.draw(self.image, 0, 0)
            self.renderEquipment("right", 0, 0)
            self.right = False
        
    def update(self):
        self.rect.x = self.x * 1
        self.rect.y = self.y * 1

    def renderEquipment(self, direction, tuple1, tuple2):
        if self.headArmor != None:
            if direction == "left":
                self.headArmor.animWalkLeft.draw(self.image, tuple1, tuple2)
            elif direction == "right":
                self.headArmor.animWalkRight.draw(self.image, tuple1, tuple2)
            elif direction == "down":
                self.headArmor.animWalkBackward.draw(self.image, tuple1, tuple2)
            elif direction == "up":
                self.headArmor.animWalkForward.draw(self.image, tuple1, tuple2)
        else:
            pass

        if self.torsoArmor != None:
            if direction == "left":
                self.torsoArmor.animWalkLeft.draw(self.image, tuple1, tuple2)
            elif direction == "right":
                self.torsoArmor.animWalkRight.draw(self.image, tuple1, tuple2)
            elif direction == "down":
                self.torsoArmor.animWalkBackward.draw(self.image, tuple1, tuple2)
            elif direction == "up":
                self.torsoArmor.animWalkForward.draw(self.image, tuple1, tuple2)
        else:
            pass

        if self.armArmor != None:
            if direction == "left":
                self.armArmor.animWalkLeft.draw(self.image, tuple1, tuple2)
            elif direction == "right":
                self.armArmor.animWalkRight.draw(self.image, tuple1, tuple2)
            elif direction == "down":
                self.armArmor.animWalkBackward.draw(self.image, tuple1, tuple2)
            elif direction == "up":
                self.armArmor.animWalkForward.draw(self.image, tuple1, tuple2)
        else:
            pass

        if self.legArmor != None:
            if direction == "left":
                self.legArmor.animWalkLeft.draw(self.image, tuple1, tuple2)
            elif direction == "right":
                self.legArmor.animWalkRight.draw(self.image, tuple1, tuple2)
            elif direction == "down":
                self.legArmor.animWalkBackward.draw(self.image, tuple1, tuple2)
            elif direction == "up":
                self.legArmor.animWalkForward.draw(self.image, tuple1, tuple2)
        else:
            pass

        if self.lWeapon != None:
            if direction == "left":
                self.lWeapon.animWalkLeft.draw(self.image, tuple1, tuple2)
            elif direction == "right":
                self.lWeapon.animWalkRight.draw(self.image, tuple1, tuple2)
            elif direction == "down":
                self.lWeapon.animWalkBackward.draw(self.image, tuple1, tuple2)
            elif direction == "up":
                self.lWeapon.animWalkForward.draw(self.image, tuple1, tuple2)
            else:
                pass

        if self.rWeapon != None:
            if direction == "left":
                self.rWeapon.animWalkLeft.draw(self.image, tuple1, tuple2)
            elif direction == "right":
                self.rWeapon.animWalkRight.draw(self.image, tuple1, tuple2)
            elif direction == "down":
                self.rWeapon.animWalkBackward.draw(self.image, tuple1, tuple2)
            elif direction == "up":
                self.rWeapon.animWalkForward.draw(self.image, tuple1, tuple2)
            else:
                pass

        
    

    def replaceBackground(self, direction):
        

        #all of the coordinates are offset because the main game map is centered in the screen
        if direction == "right":
            self.image.blit(self.background, (0, 0), (self.x - 54, self.y - 64, 64, 64)) #get the section of background where the player is and blit it onto the image
        elif direction == "left":
            self.image.blit(self.background, (0, 0), (self.x - 74, self.y - 64, 64, 64)) #get the section of background where hte player is and blit it onto the image
        elif direction == "down":
            self.image.blit(self.background, (0, 0), (self.x - 64, self.y - 54, 64, 64))
        elif direction == "up":
            self.image.blit(self.background, (0, 0), (self.x - 64, self.y - 74, 64, 64))

    def dropItem(self, item):
        print("item dropped")
        self.game.droppedItems(item)
        self.inventory.remove(item)

    def pickUpItem(self, item):
        print("item picked up")

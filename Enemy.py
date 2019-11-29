import pygame
from collections import deque
from random import randint
from spriteSheet import *
from enemy_attack import *

class Enemy(pygame.sprite.Sprite): #create enemy class

    def __init__(self, game, player, x, y, speed, name, HP, maxHP, DEX, headArmor, torsoArmor, armArmor, legArmor, classification, fileName, targetableAreas):
        self.groups = game.all_sprites

        path = "img/enemy/"+fileName+"/"+fileName

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.player = player

        self.x = x

        self.y = y

        self.name = name

        self.HP = HP

        self.maxHP = maxHP

        self.DEX = DEX

        self.headArmor = headArmor

        self.torsoArmor = torsoArmor

        self.armArmor = armArmor

        self.legArmor = legArmor

        self.classification = classification

        self.image = pygame.image.load(path+"_img.png").convert_alpha()

        self.rect = self.image.get_rect()

        

        self.rect.x = x

        self.rect.y = y

        self.speed = speed

        self.enemyWalkForward = spriteSheet(path+"_front.png", 6, 1)

        self.enemyWalkForwardList = self.enemyWalkForward.getSpriteList()

        self.walkForwardCount = 0

        self.enemyWalkBackward = spriteSheet(path+"_back.png", 6, 1)

        self.enemyWalkBackwardList = self.enemyWalkBackward.getSpriteList()

        self.walkBackwardCount = 0

        self.enemyWalkLeft = spriteSheet(path+"_left.png", 8, 1)

        self.enemyWalkLeftList = self.enemyWalkLeft.getSpriteList()

        self.walkLeftCount = 0

        self.enemyWalkRight = spriteSheet(path+"_right.png", 8, 1)

        self.enemyWalkRightList = self.enemyWalkRight.getSpriteList()

        self.walkRightCount = 0

        self.background = pygame.image.load("img/tile/chasm/chasm_01_full.png").convert() #load full background image

        basic_attack = enemy_attack("Basic Attack", 1, "Slashing", 5, 60, None, 0)

        lunge = enemy_attack("Lunge", 2, "Piercing", 6, 30, None, 0)
        
        self.attack_moves = [basic_attack, lunge]

        self.targetableAreas = targetableAreas

        self.idleAnim = path+"_idle_animation.png"

        self.hurtAnim = path+"_hit.png"

        self.attackHeadAnim = path+"_attack_head.png"

        self.attackHeadSuccessfulAnim = path+"_attack_head_successful.png"

        self.attackLeftArmAnim = path+"_attack_left_arm.png"

        self.attackLeftArmSuccessfulAnim = path+"_attack_left_arm_successful.png"

        self.attackRightArmAnim = path+"_attack_right_arm.png"

        self.attackRightArmSuccessfulAnim = path+"_attack_right_arm_successful.png"

        self.attackTorsoAnim = path+"_attack_torso.png"

        self.attackTorsoSuccessfulAnim = path+"_attack_torso_successful.png"

        self.attackLeftLegAnim = path+"_attack_left_leg.png"

        self.attackLeftLegSuccessfulAnim = path+"_attack_left_leg_successful.png"

        self.attackRightLegAnim = path+"_attack_right_leg.png"

        self.attackRightLegSuccessfulAnim = path+"_attack_right_leg_successful.png"

        self.idle_background = path+"_background.png"

        self.hurt_background = path+"_hurt_bg.png"

    def move(self):
        directionVector = pygame.math.Vector2(self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)
        directionVector.normalize()
        directionVector.scale_to_length(3)
        self.rect.move_ip(directionVector)
        self.walkAnim(directionVector.x, directionVector.y)
        


    def walkAnim(self, x, y):
        absX = abs(x)
        absY = abs(y)

        if absX > absY:
            if x < 0:
                #print("walking left")
                if self.walkLeftCount < len(self.enemyWalkLeftList):
                    leftSpriteTuple = self.enemyWalkLeftList[self.walkLeftCount]
                    self.replaceBackground("left") #DONT FORGET TO IMPLEMENT THIS!!!!
                    self.enemyWalkLeft.draw(self.image, leftSpriteTuple[0], leftSpriteTuple[1])                    
                    if self.walkLeftCount == len(self.enemyWalkLeftList) - 1:
                        self.walkLeftCount = 0
                    else:
                        self.walkLeftCount += 1
            if x > 0:
                #print("walking right")
                if self.walkRightCount < len(self.enemyWalkRightList):
                    rightSpriteTuple = self.enemyWalkRightList[self.walkRightCount]
                    self.replaceBackground("right") #DONT FORGET TO IMPLEMENT THIS!!!!
                    self.enemyWalkRight.draw(self.image, rightSpriteTuple[0], rightSpriteTuple[1])                    
                    if self.walkRightCount == len(self.enemyWalkRightList) - 1:
                        self.walkRightCount = 0
                    else:
                        self.walkRightCount += 1
        else:
            if y > 0:
                #print("walking up")
                if self.walkForwardCount < len(self.enemyWalkForwardList):
                    upSpriteTuple = self.enemyWalkForwardList[self.walkForwardCount]
                    self.replaceBackground("down")
                    self.enemyWalkForward.draw(self.image, upSpriteTuple[0], upSpriteTuple[1])
                    if self.walkForwardCount == len(self.enemyWalkForwardList) - 1:
                        self.walkForwardCount = 0
                    else:
                        self.walkForwardCount += 1
            if y < 0:
                #print("walking down")
                if self.walkBackwardCount < len(self.enemyWalkBackwardList):
                    downSpriteTuple = self.enemyWalkBackwardList[self.walkBackwardCount]
                    self.replaceBackground("up")
                    self.enemyWalkBackward.draw(self.image, downSpriteTuple[0], downSpriteTuple[1])
                    if self.walkBackwardCount == len(self.enemyWalkBackwardList) - 1:
                        self.walkBackwardCount = 0
                    else:
                        self.walkBackwardCount += 1

    def replaceBackground(self, direction):
        

        #all of the coordinates are offset because the main game map is centered in the screen
        if direction == "right":
            self.image.blit(self.background, (0, 0), (self.rect.x - 61, self.rect.y - 64, 64, 64)) #get the section of background where the player is and blit it onto the image
        elif direction == "left":
            self.image.blit(self.background, (0, 0), (self.rect.x - 67, self.rect.y - 64, 64, 64)) #get the section of background where hte player is and blit it onto the image
        elif direction == "down":
            self.image.blit(self.background, (0, 0), (self.rect.x - 64, self.rect.y - 61, 64, 64))
        elif direction == "up":
            self.image.blit(self.background, (0, 0), (self.rect.x - 64, self.rect.y - 67, 64, 64))

    def takeDamage(self, DMG):
         
        self.HP = self.HP - DMG




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

    

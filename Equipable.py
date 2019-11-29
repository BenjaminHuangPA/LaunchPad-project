import pygame
from collections import deque
from random import randint
from spriteSheet import *


class Equipable(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y, statReq, forwardSpriteSheetName, backwardSpriteSheetName, leftSpriteSheetName, rightSpriteSheetName, itemImage, equipImage, value, description):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.name = name

        self.x = x

        self.y = y

        self.statReq = statReq

        #TODO: implement description attribute

        self.type = "armor"

        self.image = pygame.image.load(itemImage).convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x

        self.rect.y = y

        self.forwardSpriteSheetName = forwardSpriteSheetName #remember: these are the FILE NAMES OF THE SPRITE SHEETS

        self.backwardSpriteSheetName = backwardSpriteSheetName

        self.leftSpriteSheetName = leftSpriteSheetName

        self.rightSpriteSheetName = rightSpriteSheetName

        self.equipImage = pygame.image.load(equipImage).convert_alpha()

        self.value = value

        self.description = description

        self.forwardSpriteSheet = None #remember: these are LISTS OF COORDINATES CORRESPONDING TO A SPRITE SHEET, NOT THE SPRITE SHEET ITSELF!!!!

        self.backwardSpriteSheet = None

        self.leftSpriteSheet = None

        self.rightSpriteSheet = None

        self.assignSpriteSheets()

    def assignSpriteSheets(self):
        self.animWalkLeft = spriteSheet(self.leftSpriteSheetName, 8, 1) #remember: these are THE SPRITE SHEET OBJECTS ON WHICH "DRAW" WILL BE CALLED

        self.animWalkRight = spriteSheet(self.rightSpriteSheetName, 8, 1)

        self.animWalkForward = spriteSheet(self.forwardSpriteSheetName, 6, 1)

        self.animWalkBackward = spriteSheet(self.backwardSpriteSheetName, 6, 1)

        self.leftSpriteSheet = self.animWalkLeft.getSpriteList()

        self.rightSpriteSheet = self.animWalkRight.getSpriteList()

        self.forwardSpriteSheet = self.animWalkForward.getSpriteList()

        self.backwardSpriteSheet = self.animWalkBackward.getSpriteList()

class Armor(Equipable):
    def __init__(self, game, displayName, x, y, dmgReduction, armorType, elemBonus, statReq, region, setName, typeName, value, description):
        path = "img/items/armor/"+setName+"/"+setName+"_"+typeName+"/"+setName+"_"+typeName
        super().__init__(game, displayName, x, y, statReq,path+"_game_back.png", path+"_game_front.png", path+"_game_left.png", path+"_game_right.png", path+"_32x32.png", path+"_game.png", value, description)
        self.dmgReduction = dmgReduction
        self.armorType = armorType
        self.elemBonus = elemBonus
        self.region = region

    def getArmorType(self):
        return self.armorType

    def getElemBonus(self):
        return self.elemBonus
    
        
class Weapon(Equipable):

    def __init__(self, game, displayName, x, y, weaponType, hand, weighting, dmgType, rawDMG, critChance, elemBonus, statReq, bonus, specAttack, fileName, value, description):
        path = "img/items/weapon/"+fileName+"/"+fileName
        super().__init__(game, displayName, x, y, statReq, path+"_back.png", path+"_front.png", path+"_left.png", path+"_right.png", path+"_32x32.png", path+"_equip.png", value, description)
        self.weaponType = weaponType
        self.hand = hand
        self.weighting = weighting
        self.dmgType = dmgType
        self.rawDMG = rawDMG
        self.critChance = critChance
        self.elemBonus = elemBonus
        self.bonus = bonus
        self.specAttack = specAttack
        self.type = "weapon"

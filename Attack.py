import pygame
from collections import deque
from random import randint
from Player import *
from Enemy import *


class Attack(object):

    def __init__(self, player, enemy, hand, magnitude, region, specificRegion, isSpecAttack, move):
        self.player = player 
        self.enemy = enemy
        self.hand = hand
        self.magnitude = magnitude #light, heavy, charged
        self.region = region #head, torso, arms or legs
        self.specificRegion = specificRegion #left arm/leg, right arm/leg
        self.isSpecAttack = isSpecAttack
        self.move = move
        

    def calculateDamage(self):
        print("Run!")
        damageWithBonus = self.getRawDamage() * self.getMagnitudeBonus()
        if self.calculateCrit():
            damageWithBonus *= 2
        totalDamage = damageWithBonus + self.calculateStrengthBonus()
        print("Total Damage:")
        print(totalDamage)
        
        armorBonus = 0
        elemBonus = 0
        
        if self.region in self.enemy.targetableAreas:
            dmgTaken = 0
            armorBonus = 0
            elemBonus = 0
            print(self.region)
            if self.hand == "Left handed attack":
                if self.player.lWeapon != None:
                    DMG_type = self.player.lWeapon.dmgType
                else:
                    DMG_type = "Blunt"
            elif self.hand == "Right handed attack":
                if self.player.rWeapon != None:
                    DMG_type = self.player.rWeapon.dmgType
                else:
                    DMG_type = "Blunt"
            elif self.hand == "Enemy attack":
                DMG_type = self.move.dmg_type
            
            if self.region == "Target: arms":
                if self.enemy.armArmor != None:
                    armorBonus = self.determineDmgTypeBonus(self.enemy.armArmor.getArmorType(), DMG_type)
                    elemBonus = self.determineElemTypeBonus(self.enemy.armArmor) 
                    dmgTaken = totalDamage - armorBonus - elemBonus
                else:
                    dmgTaken = totalDamage
            elif self.region == "Target: legs":
                if self.enemy.legArmor != None:
                    armorBonus = self.determineDmgTypeBonus(self.enemy.legArmor.getArmorType(), DMG_type)
                    elemBonus = self.determineElemTypeBonus(self.enemy.legArmor) 
                    dmgTaken = totalDamage - armorBonus - elemBonus
                else:
                    dmgTaken = totalDamage
            elif self.region == "Target: head":
                if self.enemy.headArmor != None:
                    armorBonus = self.determineDmgTypeBonus(self.enemy.headArmor.getArmorType(), DMG_type)
                    elemBonus = self.determineElemTypeBonus(self.enemy.headArmor) 
                    dmgTaken = totalDamage - armorBonus - elemBonus
                else:
                    dmgTaken = totalDamage
            elif self.region == "Target: torso":
                if self.enemy.torsoArmor != None:
                    armorBonus = self.determineDmgTypeBonus(self.enemy.torsoArmor.getArmorType(), DMG_type)
                    elemBonus = self.determineElemTypeBonus(self.enemy.torsoArmor) 
                    dmgTaken = totalDamage - armorBonus - elemBonus
                else:
                    dmgTaken = totalDamage
            print("Armor Bonus:")
            print(armorBonus)
            print("Elemental Bonus:")
            print(elemBonus)

            print("Final Damage taken:")
            print(dmgTaken)
            
            if dmgTaken < 0:
                dmgTaken = 0

            self.enemy.takeDamage(dmgTaken)

            return dmgTaken
            
            
        
        
        
    def calculateStrengthBonus(self):
        if self.player.name == "Horace":
            bonus = self.player.STR * 2
            return bonus
        else:
            return 1.2

    def getRawDamage(self):
        rawDMG = 0
        if self.player.name == "Horace":
            if self.hand == "Left handed attack":
                if self.player.lWeapon == None:
                    return self.player.STR
                else:
                    rawDMG = self.player.lWeapon.rawDMG
            elif self.hand == "Right handed attack":
                if self.player.rWeapon == None:
                    return self.player.STR
                else:
                    print(self.player.rWeapon.name)
                    print("Raw damage from weapon:")
                    print(self.player.rWeapon.rawDMG)
                    rawDMG = self.player.rWeapon.rawDMG
        else:
            rawDMG = self.move.dmg

        return rawDMG

    def getMagnitudeBonus(self):
        if self.magnitude == "Light attack":
            return 1
        
        elif self.magnitude == "Heavy attack":
            return 1.2

        elif self.magnitude == "Charged attack":
            return 1.5

    def calculateCrit(self):
        critChance = 0
        if self.player.name == "Horace":
            if self.hand == "Left handed attack":
                if self.player.lWeapon == None:
                    critChance = 5
                else:
                    critChance = self.player.lWeapon.critChance
            elif self.hand == "Right handed attack":
                if self.player.rWeapon == None:
                    critChance = 5
                else:
                    critChance = self.player.rWeapon.critChance
        else:
            critChance = self.move.crit_chance
        value = randint(0, 100)
        if value < critChance:
            return True
        else:
            return False

    def determineDmgTypeBonus(self, armorType, dmgType):
        bonus = 0
        if armorType == "Plate":
            if dmgType == "Blunt":
                bonus = 2
            elif dmgType == "Piercing":
                bonus = 3
            elif dmgType == "Slashing":
                bonus = 2
        elif armorType == "Chainmail":
            if dmgType == "Blunt":
                bonus = -2
            elif dmgType == "Piercing":
                bonus = 3
            elif dmgType == "Slashing":
                bonus = 0
        elif armorType == "Soft":
            if dmgType == "Blunt":
                bonus = -3
            elif dmgType == "Piercing":
                bonus = -4
            elif dmgType == "Slashing":
                bonus == 0
        return bonus

    def determineElemTypeBonus(self, armor):
##        bonus_elem_reduction = 0
##        for element in self.armor.getElemBonus().keys():
##            if element == dmgType:
##                bonus_elem_reduction = self.armor.elemBonus[element]
##        return bonus_elem_reduction

        dmgType = None

        total_elemental_dmg = 0

        if self.hand == "Left handed attack":
            dmgType = list(self.player.lWeapon.elemBonus.keys())[0]
            total_elemental_dmg = self.player.lWeapon.elemBonus[0]
        elif self.hand == "Right handed attack":
            dmgType = list(self.player.lWeapon.elemBonus.keys())[0]
            total_elemental_dmg = self.player.lWeapon.elemBonus[0]
        elif self.hand == "Enemy attack":
            #dmgType = move.elemental
            dmgType = self.move.elementalDamage
            
        bonus_elem_reduction = 0
        
        if dmgType == "FIRE":
            bonus_elem_reduction = armor.elemBonus["FIRE"] - armor.elemBonus["ICE"]
        elif dmgType == "ICE":
            bonus_elem_reduction = armor.elemBonus["ICE"] - armor.elemBonus["FIRE"]
        elif dmgType == "DARK":
            bonus_elem_reduction = armor.elemBonus["DARK"] - armor.elemBonus["LIGHT"]
        elif dmgType == "LIGHT":
            bonus_elem_reduction = armor.elemBonus["LIGHT"] - armor.elemBonus["DARK"]
        else:
            bonus_elem_reduction = 0

        total_elemental_dmg = total_elemental_dmg - bonus_elem_reduction

        return total_elemental_dmg
    

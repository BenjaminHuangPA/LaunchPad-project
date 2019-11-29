import pygame
from collections import deque
from random import randint

class enemy_attack(object):

    def __init__(self, name, dmg, dmg_type, crit_chance, hit_chance, elemental, elementalDamage):
        self.name = name
        self.dmg = dmg
        self.dmg_type = dmg_type
        self.crit_chance = crit_chance
        self.hit_chance = hit_chance
        self.elemental = elemental
        self.elementalDamage = elementalDamage


    def getDMG(self):
        return self.dmg

    def getDMGType(self):
        return self.dmg_type

    def critDeterminer(self):
        chance = randint(0, 100)
        if chance < self.crit_chance:
            return True
        else:
            return False

    def hitDeterminer(self):
##        chance = randint(0, 100)
##        if chance < self.hit_chance:
##            return True
##        else:
##            return False
        return True

    def getElemental(self):
        return self.elemental

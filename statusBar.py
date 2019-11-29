import pygame
from collections import deque
from random import randint
from Player import *

class statusBar(pygame.sprite.Sprite):
    def __init__(self, game, player, x, y):
        self.groups = game.status_bar
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.player = player

        self.x = x

        self.y = y

        self.image = pygame.image.load("img/menu/statusBar.png").convert()

        self.rect = self.image.get_rect()

        self.rect.x = x * 1

        self.rect.y = y * 1

        self.healthBarRect = pygame.Rect(180, 34, 150, 11)

        self.staminaBarRect = pygame.Rect(210, 63, 120, 11)

        pygame.draw.rect(self.image, (141, 42, 42), self.healthBarRect)

        pygame.draw.rect(self.image, (35, 35, 202), self.staminaBarRect)

        self.renderPlayerAttributes()
    

        
    def increaseHealth(self):
        print(self.player.HP)
        if(self.player.HP < self.player.maxHP):
            newHealth = pygame.Rect(180, 34, 3 * self.player.HP, 11)
            pygame.draw.rect(self.image, (141, 42, 42), newHealth)
        else:
            fullHP = pygame.Rect(180, 34, 3 * self.player.maxHP, 11)
            pygame.draw.rect(self.image, (141, 42, 42), fullHP)
            

    def decreaseHealth(self):
        print(self.player.HP)
        if(self.player.HP > 0):
            remainingHP = (self.player.HP) * 3
            maxHP = (self.player.maxHP - self.player.HP) * 3
            healthLost = pygame.Rect(180 + remainingHP, 34, maxHP, 11)
            pygame.draw.rect(self.image, (82, 51, 46), healthLost)
        else:
            noHP = pygame.Rect(180, 34, self.player.maxHP * 3, 11)
            pygame.draw.rect(self.image, (82, 51, 46), noHP)

    def renderPlayerAttributes(self):
        pygame.font.init()

        font1 = pygame.font.SysFont("Times New Roman", 20)

        strength = font1.render(str(self.player.STR), False, (198, 187, 187))
        agility = font1.render(str(self.player.AGL), False, (198, 187, 187))
        intelligence = font1.render(str(self.player.INT), False, (198, 187, 187))
        dexterity = font1.render(str(self.player.DEX), False, (198, 187, 187))
        guard = font1.render(str(self.player.GRD), False, (198, 187, 187))

        self.image.blit(strength, (158, 87))
        self.image.blit(agility, (165, 106))
        self.image.blit(intelligence, (157, 126))
        self.image.blit(dexterity, (273, 87))
        self.image.blit(guard, (274, 107))

    def updateBonuses(self):
        pygame.font.init()

        font1 = pygame.font.SysFont("Times New Roman", 12)\

        blank = pygame.image.load("img/misc/blank_bonus.png").convert_alpha()
        
        armorElemBonuses = self.player.getElemDef()

        lWeaponElemBonuses = self.player.getElemATTKLeft()

        rWeaponElemBonuses = self.player.getElemATTKRight()

        resistance_x = 473
        resistance_y = 36
        for resistance in armorElemBonuses:
            self.image.blit(blank, (resistance_x, resistance_y))
            if resistance < 0:
                resistanceText = font1.render(str(resistance), False, (242, 35, 12))
            elif resistance > 0:
                resistanceText = font1.render(str(resistance), False, (52, 235, 58))
            else:
                resistanceText = font1.render(str(resistance), False, (255, 255, 255))
            self.image.blit(resistanceText, (resistance_x, resistance_y))
            resistance_y += 16

        l_attk_bonus_x = 424
        l_attk_bonus_y = 36

        r_attk_bonus_x = 443
        r_attk_bonus_y = 36

        for bonus in range(0, 4):
            self.image.blit(blank, (l_attk_bonus_x, l_attk_bonus_y))
            self.image.blit(blank, (r_attk_bonus_x, r_attk_bonus_y))
            l_bonus = lWeaponElemBonuses[bonus]
            r_bonus = rWeaponElemBonuses[bonus]
            if l_bonus < 0:
                l_bonus_text = font1.render(str(l_bonus), False, (242, 35, 12))
            elif lWeaponElemBonuses[bonus] > 0:
                l_bonus_text = font1.render(str(l_bonus), False, (52, 235, 58))
            else:
                l_bonus_text = font1.render(str(l_bonus), False, (255, 255, 255))
                
            if r_bonus < 0:
                r_bonus_text = font1.render(str(r_bonus), False, (242, 35, 12))
            elif lWeaponElemBonuses[bonus] > 0:
                r_bonus_text = font1.render(str(r_bonus), False, (52, 235, 58))
            else:
                r_bonus_text = font1.render(str(r_bonus), False, (255, 255, 255))

            self.image.blit(l_bonus_text, (l_attk_bonus_x, l_attk_bonus_y))
            self.image.blit(r_bonus_text, (r_attk_bonus_x, r_attk_bonus_y))

            l_attk_bonus_y += 16
            r_attk_bonus_y += 16

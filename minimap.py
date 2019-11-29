import pygame
from Player import *

class Minimap(pygame.sprite.Sprite):
    def __init__(self, game, x, y, name, player):
        self.groups = game.minimap_group

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.x = x

        self.y = y

        self.image = pygame.image.load("img/menu/minimap_frame.png").convert_alpha()

        self.horace_icon = pygame.image.load("img/menu/horace_minimap_icon.png").convert_alpha()
        
        self.rect = self.image.get_rect()

        self.rect.x = x * 1

        self.rect.y = y * 1

        self.player = player

        self.map = None

        self.displayMap()

        self.renderHorace()

    def displayMap(self):
        if self.player.current_zone == 1:
            self.map = pygame.image.load("img/menu/zone_1_map.png").convert_alpha()

        self.image.blit(self.map, (8, 8), (0, 0, 128, 128))

    def renderHorace(self):
        location = self.player.roomLocation
        self.image.blit(self.map, (8, 8), (0, 0, 128, 128))
        horace_location = (0, 0)
        if location == [5, 1]:
            horace_location = (67, 89)
        elif location == [5, 2]:
            horace_location = (84, 89)
        elif location == [6, 1]:
            horace_location = (68, 105)
        elif location == [4, 1]:
            horace_location = (65, 69)
        self.image.blit(self.horace_icon, horace_location, (0, 0, 8, 8))

    
    def updateLocation(self):
        self.renderHorace()
        
        

        

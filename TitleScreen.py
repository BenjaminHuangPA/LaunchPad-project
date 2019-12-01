
import pygame
from collections import deque
from random import randint

class TitleScreen(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.title_screen
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.x = x

        self.y = y

        self.image = pygame.image.load("img/misc/title_screen.png").convert_alpha()

        self.bg = pygame.image.load("img/misc/title_screen_bg.png").convert_alpha()

        self.new_game_button = pygame.image.load("img/misc/new_game_button.png").convert_alpha()

        self.new_game_button_selected = pygame.image.load("img/misc/new_game_button_selected.png").convert_alpha()

        self.load_game_button = pygame.image.load("img/misc/load_game.png").convert_alpha()

        self.load_game_button_selected = pygame.image.load("img/misc/load_game_selected.png").convert_alpha()        

        self.how_to_play_button = pygame.image.load("img/misc/how_to_play.png").convert_alpha()

        self.how_to_play_button_selected = pygame.image.load("img/misc/how_to_play_selected.png").convert_alpha()

        self.quit_button = pygame.image.load("img/misc/quit.png").convert_alpha()

        self.quit_button_selected = pygame.image.load("img/misc/quit_selected.png").convert_alpha()

        self.new_game_pos = pygame.Rect(297, 228, 177, 37)
        self.load_game_pos = pygame.Rect(297, 269, 177, 37)
        self.how_to_play_pos = pygame.Rect(297, 315, 177, 37)
        self.quit_game_pos = pygame.Rect(297, 355, 177, 37)

        self.current_selection = None

        self.current_rect = None

        self.rect = self.image.get_rect()

        self.rect.x = x

        self.rect.y = y

        self.playSound = True

        self.button_mouseover_sound = pygame.mixer.Sound("music/rollover4.ogg")
        

    def buttonMouseOver(self, pos):
        if self.new_game_pos.collidepoint(pos):
            self.selectButton(self.new_game_button_selected, self.new_game_pos)
            self.current_selection = self.new_game_button
            self.current_rect = self.new_game_pos
            
        elif self.load_game_pos.collidepoint(pos):
            self.selectButton(self.load_game_button_selected, self.load_game_pos)
            self.current_selection = self.load_game_button
            self.current_rect = self.load_game_pos

            
        elif self.how_to_play_pos.collidepoint(pos):
            self.selectButton(self.how_to_play_button_selected, self.how_to_play_pos)
            self.current_selection = self.how_to_play_button
            self.current_rect = self.how_to_play_pos

            
        elif self.quit_game_pos.collidepoint(pos):
            self.selectButton(self.quit_button_selected, self.quit_game_pos)
            self.current_selection = self.quit_button
            self.current_rect = self.quit_game_pos
        else:
            self.deselectButton(self.current_selection, self.current_rect)
        

    def selectButton(self, selectedButton, pos_rect):
        if self.playSound == True:
            self.button_mouseover_sound.play()
        self.playSound = False
        self.image.blit(self.bg, (pos_rect.left, pos_rect.top), (pos_rect.left, pos_rect.top, 177, 37))
        self.image.blit(selectedButton, (pos_rect.left, pos_rect.top), (0, 0, 177, 37))

    def deselectButton(self, button, pos_rect):
        if self.current_selection != None:
            self.image.blit(self.bg, (pos_rect.left, pos_rect.top), (pos_rect.left, pos_rect.top, 177, 37))
            self.image.blit(button, (pos_rect.left, pos_rect.top), (0, 0, 177, 37))
        self.playSound = True
    
    def clickButton(self, pos):
        if self.new_game_pos.collidepoint(pos):
            pygame.mixer.music.stop()
            return 1
        elif self.load_game_pos.collidepoint(pos):
            
            return 2
            
        elif self.how_to_play_pos.collidepoint(pos):
            
            return 3
            
        elif self.quit_game_pos.collidepoint(pos):
            return 4

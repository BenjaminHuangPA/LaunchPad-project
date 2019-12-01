import pygame
from collections import deque
from random import randint
from Player import *
from Button import *
     
class inventoryGUI(pygame.sprite.Sprite): #inventory GUI class 
    def __init__(self, game, player, x, y):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.player = player #pass in the player (to get his inventory)

        self.x = x

        self.y = y

        self.image = pygame.image.load("img/menu/inventory_gui_2_nobuttons.png").convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x * 1

        self.rect.y = y * 1

        #initialize various button objects

        self.dropButton = Button(self.game, 20, 298, "drop", "img/menu/drop_button.png", 64, 128)

        self.useButton = Button(self.game, 121, 297, "use", "img/menu/use_button.png", 64, 128)

        self.equipButton = Button(self.game, 315, 297, "equip", "img/menu/equip_button.png", 64, 128)

        self.inspectButton = Button(self.game, 222, 297, "inspect", "img/menu/inspect_button.png", 64, 128)

        self.sellButton = Button(self.game, 315, 265, "sell", "img/menu/sell_button.png", 64, 128)

        self.initializeButtons() #blit buttons to screen
    
        self.fill() #fill the inventory grid with item sprites (See below)

        self.currentSelection = 0 #initialize variable to hold the currently selected item

        self.previousSelection = 0 #initialize variable to hold the previously selected item (for blitting purposes)

        self.currentEquipmentSelection = None

        self.selectionImage = pygame.image.load("img/menu/selected.png").convert_alpha() #load the image to show that an item is selected (red border)

        self.deselectionImage = pygame.image.load("img/menu/deselected.png").convert_alpha() #load the image to show that an item has been "deselected" (plain background with no red border)
        

    def fill(self): #fill the inventory window with the player's items' sprites
        x = 24
        y = 22
        for item in self.player.inventory:
            self.image.blit(item.image, (x, y)) #blit each inventory item's sprite onto the window's image
            item.x = x #set each item's x to be the image's coordinates in the GUI (for selection purposes)
            item.y = y #set each item's y to be the image's coordinates in the GUI (for selection purposes)
            x += 34 #increment the x coordinate by 34 to draw the next item in the next box over
            if x == 262: 
                x = 24
                y += 34            #if reached the end of the row, go to the next row

    def initializeButtons(self): #blit button sprites to the screen
        self.image.blit(self.dropButton.image, (self.dropButton.x, self.dropButton.y))
        self.image.blit(self.equipButton.image, (self.equipButton.x, self.equipButton.y))
        self.image.blit(self.inspectButton.image, (self.inspectButton.x, self.inspectButton.y))
        self.image.blit(self.sellButton.image, (self.sellButton.x, self.sellButton.y))
        self.image.blit(self.useButton.image, (self.useButton.x, self.useButton.y))


    def select(self, item):
        self.previousSelection = self.currentSelection #set the currently selected image (now the previously selected image) to the variable previousSelection
        self.image.blit(self.selectionImage, (item.x, item.y)) #blit the red background over the newly selected image to visually show that it has been selected
        self.image.blit(item.image, (item.x, item.y)) #re-blit the item's image to the screen 
        self.currentSelection = item #set the currentSelection variable to the newly selected image
        if self.previousSelection != 0:
            self.deselect(self.previousSelection) #don't deselect the previous item if there was no previously deselected item
        

    def deselect(self, item):
        self.image.blit(self.deselectionImage, (self.previousSelection.x, self.previousSelection.y)) #for the previously selected item, blit the plain grey background (erases the red one)
        self.image.blit(item.image, (item.x, item.y)) #reblit the previously selected item's image

    def inspect(self): #308, 22


        testTextWrapper = textWrapper()
        
        #this method is run as a result of clicking the "inspect" button
        if(self.currentSelection == 0):
            print("Cannot inspect nothing!") #make sure I'm not accessing a thing that isn't of the item class
        else:
            pygame.font.init() #call init to use pygame's font module
            inspectionWindow = pygame.image.load("img/menu/inspection_window.png").convert() #load inspection window's image
            
            font1 = pygame.font.SysFont('Times New Roman', 9) #create new font object 
            
            name = font1.render(self.currentSelection.name, False, (255, 255, 255)) #create name text for the currently selected object to inspect
            desc = font1.render(self.currentSelection.description, False, (255, 255, 255)) #create description text for the currently selected object to inspect
            #value = font1.render(self.currentSelection.value, False, (255, 255, 255))
            
            inspectionWindow.blit(name, (56, 161)) #blit name/desc text to the inspectionWindow image

            #inspectionWindow.blit(desc, (24, 205))

            testTextWrapper.blitText(inspectionWindow, 24, 205, self.currentSelection.description, 200, 9, 11, (198, 187, 187))

            if(self.currentSelection.type == "armor"):
                scaledImage = pygame.transform.scale(self.currentSelection.equipImage, (128, 128))
            else:
                scaledImage = pygame.transform.scale(self.currentSelection.image, (128, 128))
            inspectionWindow.blit(scaledImage, (24, 24))
            
            #inspectionWindow.blit(value, (98, 256))
            self.image.blit(inspectionWindow, (308, 22)) #blit inspectionWindow image to screen
        
    def equip(self):
        if self.currentSelection.type != "armor" and self.currentSelection.type != "weapon":
            print("Cannot equip that item!")
        else:
            if self.player.canEquip(self.currentSelection) == True:
                if self.currentSelection.type == "armor":
                    if self.currentSelection.region == "head":
                        self.image.blit(self.currentSelection.equipImage, (422, 35))
                        print("Helmet equipped!")
                    elif self.currentSelection.region == "torso":
                        self.image.blit(self.currentSelection.equipImage, (422, 114))
                        print("Chestplate equipped!")
                    elif self.currentSelection.region == "arms":
                        self.image.blit(self.currentSelection.equipImage, (422, 197))
                        print("Gauntlets equipped!")
                    elif self.currentSelection.region == "legs":
                        self.image.blit(self.currentSelection.equipImage, (422, 280))
                        print("Greaves equipped!")
                    print("Name: " + self.currentSelection.name)
                    self.player.equipArmor(self.currentSelection)
                elif self.currentSelection.type == "weapon":
                    if self.currentSelection.hand == "left":
                        self.image.blit(self.currentSelection.equipImage, (318, 100))
                    elif self.currentSelection.hand == "right":
                        self.image.blit(self.currentSelection.equipImage, (318, 182))

                    self.player.equipWeapon(self.currentSelection)
            else:
                if self.player.canEquip(self.currentSelection) != True:
                    message = "Your " + self.player.canEquip(self.currentSelection) + " is not high enough to equip this item."
                    statBox = messageBox(self.game, self.player, 66, 128, message)

    def drop(self):
        #drop items
        self.player.dropItem(self.currentSelection)
        blank_inventory = pygame.image.load("img/menu/blank_inventory.png").convert_alpha()
        self.image.blit(blank_inventory, (22, 20))
        self.fill()
            
                
                

    def selectEquipment(self, slot):
        equipmentSelected = pygame.image.load("img/menu/equipment_selected.png").convert_alpha()
        if slot == "head" and self.player.headArmor != None:
            self.image.blit(equipmentSelected, (406, 18))
            self.currentEquipmentSelection = "head"
        elif slot == "torso" and self.player.torsoArmor != None:
            self.image.blit(equipmentSelected, (406, 200))
            self.currentEquipmentSelection = "torso"
        elif slot == "arms" and self.player.armArmor != None:
            self.image.blit(equipmentSelected, (406, 182))
            self.currentEquipmentSelection = "arms"
        elif slot == "legs" and self.player.legArmor != None:
            self.image.blit(equipmentSelected, (406, 164))
            self.currentEquipmentSelection = "legs"
        elif slot == "lweapon" and self.player.lWeapon != None:
            self.image.blit(equipmentSelected, (318, 100))
            self.currentEquipmentSelection = "lweapon"
        elif slot == "rweapon" and self.player.rWeapon != None:
            self.image.blit(equipmentSelected, (319, 182))
            self.currentEquipmentSelection = "rweapon"
            
        self.equipButton.image = pygame.image.load("img/menu/unequip_button.png").convert_alpha()

        self.initializeButtons()

       

    def unequip(self):
        print("unequip method run")
        equipmentUnselected = pygame.image.load("img/menu/nothing_equipped.png").convert_alpha()
        
        if self.currentEquipmentSelection == "head":
            self.player.unequipArmor("head")
            self.image.blit(equipmentUnselected, (406, 18))
        elif self.currentEquipmentSelection == "torso":
            self.player.unequipArmor("torso")
            self.image.blit(equipmentUnselected, (406, 200))
        elif self.currentEquipmentSelection == "arms":
            self.player.unequipArmor("arms")
            self.image.blit(equipmentUnselected, (406, 182))
        elif self.currentEquipmentSelection == "legs":
            self.player.unequipArmor("legs")
            self.image.blit(equipmentUnselected, (406, 164))
        elif self.currentEquipmentSelection == "lweapon":
            self.player.unequipWeapon("lweapon")
            self.image.blit(equipmentUnselected, (318, 100))
        elif self.currentEquipmentSelection == "rweapon":
            self.player.unequipWeapon("rweapon")
            self.image.blit(equipmentUnselected, (318, 182))
            

        self.equipButton.image = pygame.image.load("img/menu/equip_button.png").convert_alpha()

        self.initializeButtons()

        self.currentEquipmentSelection = None

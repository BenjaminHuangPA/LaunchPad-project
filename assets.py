
import pygame



class Player(pygame.sprite.Sprite):
    
    def __init__(self, game, x, y, inventory, HP, maxHP, STM, maxSTM, STR, AGL, INT, DEX, GRD, headArmor, torsoArmor, armArmor, legArmor):
        self.groups = game.all_sprites, game.entities #set the player's sprite group to all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.roomLocation = [5, 1] #denote where in the gameloop's 2d zone array the player is. i.e. index 1 of array 5.

        self.image = pygame.image.load("test.png").convert_alpha() #.convert_alpha() enables png transparency

        self.rect = self.image.get_rect() #how pygame knows where to draw the sprite (VERY IMPORTANT)
        #get rect returns the size of the sprite's image

        self.x = x

        self.y = y

        #note: pygame relies on three attributes to know where to draw sprites: the sprite's self.x, self.y and self.rect

        self.forward = False

        self.forward = True

        self.left = False

        self.right = False

        #self.speed = 10

        self.playerWalkLeft = spriteSheet("horace_idle_left_side.png", 8, 1) #initialize spriteSheet object for the player walking to the left

        self.playerWalkLeftList = self.playerWalkLeft.getSpriteList() #get list of coordinates representing the upper left corners of the individiual sprites in the spriteSheet

        self.walkLeftCount = 0 

        self.playerWalkRight = spriteSheet("horace_idle_side.png", 8, 1) #initialize spriteSheet object for the player walking to the right

        self.playerWalkRightList = self.playerWalkRight.getSpriteList()

        self.walkRightCount = 0 

        self.playerWalkForward = spriteSheet("horace_idle_back.png", 6, 1)

        self.playerWalkForwardList = self.playerWalkForward.getSpriteList() #initialize spriteSheet object for the player walking forward

        self.walkForwardCount = 0

        self.playerWalkBackward = spriteSheet("horace_idle.png", 6, 1)

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
        
        

    def move(self, x, y):
        
        #if(self.checkWallCollision() == True):
        self.walkAnim(x, y) #play the walking animation (See below)
        self.x += x #move player left/right
        self.y += y #move player right/left

    def takeDamage(self, DMG):
        self.HP = self.HP - DMG

    def heal(self, HP):
        self.HP = self.HP + HP

    def equipArmor(self, armor):
        if armor.region == "head":
            self.headArmor = armor
        elif armor.region == "torso":
            self.torsoArmor = armor
        elif armor.region == "arms":
            self.armArmor = armor
        elif armor.region == "legs":
            self.legArmor = armor

    def unequipArmor(self, region):
        if region == "head":
            self.headArmor = None
        elif region == "torso":
            self.torsoArmor = None
        elif region == "arms":
            self.armArmor = None
        elif region == "legs":
            self.legArmor = None
        
    def walkAnim(self, x, y):
        if x < 0: #if the player walks to the left (change in x pos less than 0)
            if self.walkLeftCount < len(self.playerWalkLeftList): #loop through the list of sprites of the player walking
                leftSpriteTuple = self.playerWalkLeftList[self.walkLeftCount] #
                self.replaceBackground("left") #call blitOut2 method to blit new blank background onto the image
                self.playerWalkLeft.draw(self.image, leftSpriteTuple[0], leftSpriteTuple[1]) #call the sprite class instance's draw method to blit the correct sprite onto the image
                self.renderArmor("left", leftSpriteTuple[0], leftSpriteTuple[1])
                if self.walkLeftCount == len(self.playerWalkLeftList) - 1: 
                    self.walkLeftCount = 0 #if reached the end of the array of sprites, start over at the beginning
                else:
                    self.walkLeftCount += 1 #else, go to the next sprite
        
        if x > 0: #handle walking right
            if self.walkRightCount < len(self.playerWalkRightList):
                rightSpriteTuple = self.playerWalkRightList[self.walkRightCount]
                self.replaceBackground("right")
                self.playerWalkRight.draw(self.image, rightSpriteTuple[0], rightSpriteTuple[1])
                self.renderArmor("right", rightSpriteTuple[0], rightSpriteTuple[1])
                if self.walkRightCount == len(self.playerWalkRightList) - 1:
                    self.walkRightCount = 0
                else:
                    
                    self.walkRightCount += 1
        if y > 0:
            if self.walkBackwardCount < len(self.playerWalkBackwardList):
                downSpriteTuple = self.playerWalkBackwardList[self.walkBackwardCount]
                self.replaceBackground("down")
                self.playerWalkBackward.draw(self.image, downSpriteTuple[0], downSpriteTuple[1])
                self.renderArmor("down", downSpriteTuple[0], downSpriteTuple[1])
                if self.walkBackwardCount == len(self.playerWalkBackwardList) - 1:
                    self.walkBackwardCount = 0
                else:
                    self.walkBackwardCount += 1
        if y < 0:
            if self.walkForwardCount < len(self.playerWalkForwardList):
                upSpriteTuple = self.playerWalkForwardList[self.walkForwardCount]
                self.replaceBackground("up")
                self.playerWalkForward.draw(self.image, upSpriteTuple[0], upSpriteTuple[1])
                self.renderArmor("up", upSpriteTuple[0], upSpriteTuple[1])
                if self.walkForwardCount == len(self.playerWalkForwardList) - 1:
                    self.walkForwardCount = 0
                else:
                    self.walkForwardCount += 1
        #pygame.display.update()

        
    def update(self):
        self.rect.x = self.x * 1
        self.rect.y = self.y * 1

    def renderArmor(self, direction, tuple1, tuple2):
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

    

    def replaceBackground(self, direction):
        
        background = pygame.image.load("chasm_01_full.png").convert() #load full background image

        #all of the coordinates are offset because the main game map is centered in the screen
        if direction == "right":
            self.image.blit(background, (0, 0), (self.x - 54, self.y - 64, 64, 64)) #get the section of background where the player is and blit it onto the image
        elif direction == "left":
            self.image.blit(background, (0, 0), (self.x - 74, self.y - 64, 64, 64)) #get the section of background where hte player is and blit it onto the image
        elif direction == "down":
            self.image.blit(background, (0, 0), (self.x - 64, self.y - 54, 64, 64))
        elif direction == "up":
            self.image.blit(background, (0, 0), (self.x - 64, self.y - 74, 64, 64))

class spriteSheet(object): #create spriteSheet class to handle sprite sheets
    def __init__(self, filename, cols, rows): #constructor with arguments filename, rows, and columns
        self.sheet = pygame.image.load(filename).convert_alpha() #load the spritesheet
        
        self.cols = cols 
        self.rows = rows
        self.totalCellCount = cols * rows #get total number of cells based on rows/columns

        self.rect = self.sheet.get_rect() #get the area of the sprite sheet
        w = self.cellWidth = self.rect.width / cols #each cell's width is the whole sheet's width divided by the number of columns
        h = self.cellHeight = self.rect.height / rows #each cell's height is the whole sheet's height divided by the number of rows


    def getSpriteList(self):
        x = 0
        y = 0
        spriteList = [] #initialize list to hold sprite coordinates in
        for row in range(0, self.rows): #for each row in the sprite sheet:
            for column in range(0, self.cols): #for each column in the sprite sheet:
                coords = (x, y) #create tuple of the x and y from above
                spriteList.append(coords) #append to list
                x -= self.cellWidth #increment x by the width of each cell 
            y -= self.cellHeight #then when going to the next row, increment the y by the height of a cell
        return spriteList #return the list

        
    def draw(self, surface, x, y):
        surface.blit(self.sheet, (x, y, self.cellWidth, self.cellHeight))

class Armor(pygame.sprite.Sprite):
    def __init__(self, game, name, x, y, region, forwardSpriteSheetName, backwardSpriteSheetName, leftSpriteSheetName, rightSpriteSheetName, itemImage, equipImage, value, description):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.name = name

        self.x = x

        self.y = y

        self.region = region

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
    

class Tile(pygame.sprite.Sprite): #create class for the tile (child class of pygame.sprite.Sprite
    def __init__(self, game, x, y, background):
        self.groups = game.all_sprites, game.all_tiles #set this sprite's groups to
        #the all_sprites and tiles groups created in the main file's main method.
        pygame.sprite.Sprite.__init__(self, self.groups)#call parent class constructor
        self.game = game

        #all images in pygame are called "surfaces"
        #self.image = pygame.Surface((64, 64))

        self.image = pygame.image.load(background).convert()

        #self.image.fill((0, 255, 0)) #make each tile green (for now)

        self.rect = self.image.get_rect() #get rectangular area of the surface

        self.x = x

        self.y = y

        self.rect.x = x * 64

        self.rect.y = y * 64

class Door(pygame.sprite.Sprite):
    def __init__ (self, game, x, y, orientation, status, spriteImage, bgImage):
        self.groups = game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.spriteImage = spriteImage

        self.bgImage = bgImage #get the background wall's image so we can blit over the open doors once they're no longer open

        self.image = pygame.image.load(spriteImage).convert()

        self.rect = self.image.get_rect()

        self.x = x

        self.y = y

        self.orientation = orientation #denotes if the door is "forward", "backward", "left", or "right"

        self.status = status #denotes if the door is open or closed (True is open, False is closed)

        #self.image = spriteImage

        if self.status == False:
            self.image = pygame.image.load("door_blocked.png").convert()

        self.rect.x = x * 64

        self.rect.y = y * 64

    #these two methods change the door's appearance to show that it's shut or open

    def closeDoor(self):
        bgWall = pygame.image.load(self.bgImage).convert()
        print(self.x)
        print(self.y)
        if self.orientation == "right":
            self.image.blit(bgWall, (0, 0), (0, self.y * 64, 64, 64))
        elif self.orientation == "left":
            self.image.blit(bgWall, (0, 0), (0, self.y * 64, 64, 64))
        elif self.orientation == "forward":
            self.image.blit(bgWall, (0, 0), (self.x * 64, 0, 64, 64))
        elif self.orientation == "backward":
            self.image.blit(bgWall, (0, 0), (self.x * 64, 0, 64, 64))

    def openDoor(self):
        self.image = pygame.image.load(self.spriteImage).convert()

    

class Room(object):
    def __init__(self, game, base, door, background, props):
        self.base = base
        self.door = door #list of doors that this room has
        self.game = game 

        self.background = background #filename of the background image for this room's tiles

        self.doors = door

        rows, cols = (8, 8)

        self.props = props

        #initialize array the manual way
        self.tiles = [[0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0]]

        

        x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for x in range(0, 8):
            for y in range(0, 8):
                self.tiles[x][y] = Tile(self.game, x1[x], x1[y], background) #fill the 2d array with tile objects 
        
        
class item(pygame.sprite.Sprite):
    def __init__(self, game, x, y, image, name, value, description, isConsumable, rarity, ID):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.game = game

        self.x = x

        self.y = y

        self.type = "item"

        self.image = pygame.image.load(image).convert()

        self.name = name

        self.value = value

        self.description = description

        self.isConsumable = isConsumable

        self.rarity = rarity

        self.ID = ID

        self.rect = self.image.get_rect()

        self.rect.x = 32 

        self.rect.y = 32

class Prop(pygame.sprite.Sprite):
    def __init__(self, x, y, name, value, isInteractable, spriteImage):

        #self.game = game

        #self.groups = game.props

        pygame.sprite.Sprite.__init__(self)

        #self.game = game

        self.x = x

        self.y = y

        self.image = pygame.image.load(spriteImage).convert_alpha()

        self.rect = self.image.get_rect()

        self.name = name

        self.value = value

        self.isInteractable = isInteractable

        self.rect.x = x

        self.rect.y = y

    

        

class Button(pygame.sprite.Sprite): #define button class for the inventory GUI
    def __init__(self, game, x, y, functionality, image, xOffset, yOffset):
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.x = x

        self.y = y

        self.functionality = functionality #variable to describe what the button does

        self.image = pygame.image.load(image).convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x + xOffset

        self.rect.y = y + yOffset

class statusBar(pygame.sprite.Sprite):
    def __init__(self, game, player, x, y):
        self.groups = game.status_bar
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.player = player

        self.x = x

        self.y = y

        self.image = pygame.image.load("statusBar.png").convert()

        self.rect = self.image.get_rect()

        self.rect.x = x * 1

        self.rect.y = y * 1

        self.healthBarRect = pygame.Rect(180, 34, 150, 11)

        self.staminaBarRect = pygame.Rect(210, 63, 120, 11)

        pygame.draw.rect(self.image, (141, 42, 42), self.healthBarRect)

        pygame.draw.rect(self.image, (35, 35, 202), self.staminaBarRect)

        self.renderPlayerAttributes()

        
    def increaseHealth(self, health):
        print(self.player.HP)
        if(self.player.HP < self.player.maxHP):
            newHealth = pygame.Rect(180, 34, 3 * self.player.HP, 11)
            pygame.draw.rect(self.image, (141, 42, 42), newHealth)
        else:
            fullHP = pygame.Rect(180, 34, 3 * self.player.maxHP, 11)
            pygame.draw.rect(self.image, (141, 42, 42), fullHP)
            

    def decreaseHealth(self, health):
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


class textWrapper(object):

    #The purpose of this class is thus: Pygame does not natively implement a way
    #to write text on multiple lines, and new line characters are ignored. Thus,
    #I wrote this class to format text that would be too long to fit a given width
    #into a paragraph.

    
    def __init__(self):
        pass #no need to pass anything into the constructor

    def blitText(self, surface, x, y, text, width, font_size, line_height, color):
        R = color[0]

        G = color[1] #pass in the color as an RGB tuple

        B = color[2]

        pygame.font.init() #initialize pygame's font module

        textArray = text.split() #split the inputted text into separate words

        font = pygame.font.SysFont("Times New Roman", font_size) #initialize font object using the font size module

        yCoord = y #this variable will store the y coordinate of the lines we draw the text on.

        currentLineLength = 0 #this variable will store the length of the current line of text, for checking if we've exceeded the target width.

        textToDraw = "" #this variable (initialized to an empty String) will store the text to be written for each line.

        textSize = font.size(text) #this method returns a tuple of its argument's dimensions in the form (width, height)
        if textSize[0] < width:
            #check if the text passed in is no more than a single line's worth. If that's the case, we can just blit it directly to the surface without having to worry about
            #new lines
            line = font.render(text, False, (R, G, B))
            surface.blit(line, (x, yCoord))
        else:
            #now we need to handle if the text passed in has a length greater than a single line
            for word in textArray:
                wordSize = font.size(word) #get the tuple describing each word's dimensions
                wordLength = wordSize[0] + 15 #get the word's length. Add +15 pixels to account for spaces.
                
                if currentLineLength + wordLength < width:
                    currentLineLength += wordLength
                    textToDraw = textToDraw + word + " "
                    #if we can add this word to the current line of text to be drawn (textToDraw) without exceeding the width of a single line, do so
                elif currentLineLength + wordLength > width:
                    #else, if adding the word would go over the limit imposed:
                    line = font.render(textToDraw, False, (R, G, B)) #render the text onto a surface
                    surface.blit(line, (x, yCoord)) #draw the surface containing the text onto the surface passed in
                    yCoord += line_height #increment yCoord to go to a new line.
                    currentLineLength = wordLength  #add the word's length to the currentLineLength variabel
                    textToDraw = word + " " #move the word that would have caused the line of text to go over the width to the start of the new line.
       
        lastLine = font.render(textToDraw, False, (R, G, B)) #finally, blit the last line of text onto the screen (which is almost always shorter than width and as a result is
        #not drawn by the above if statement
        surface.blit(lastLine, (x, yCoord))
            
        
            
        

class inventoryGUI(pygame.sprite.Sprite): #inventory GUI class 
    def __init__(self, game, player, x, y):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.player = player #pass in the player (to get his inventory)

        self.x = x

        self.y = y

        self.image = pygame.image.load("inventory_gui_2_nobuttons.png").convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x * 1

        self.rect.y = y * 1

        #initialize various button objects

        self.dropButton = Button(self.game, 20, 298, "drop", "drop_button.png", 64, 128) 

        self.useButton = Button(self.game, 121, 297, "use", "use_button.png", 64, 128)

        self.equipButton = Button(self.game, 315, 297, "equip", "equip_button.png", 64, 128)

        self.inspectButton = Button(self.game, 222, 297, "inspect", "inspect_button.png", 64, 128)

        self.sellButton = Button(self.game, 315, 265, "sell", "sell_button.png", 64, 128)

        self.initializeButtons() #blit buttons to screen
    
        self.fill() #fill the inventory grid with item sprites (See below)

        self.currentSelection = 0 #initialize variable to hold the currently selected item

        self.previousSelection = 0 #initialize variable to hold the previously selected item (for blitting purposes)

        self.currentEquipmentSelection = None

        self.selectionImage = pygame.image.load("selected.png").convert_alpha() #load the image to show that an item is selected (red border)

        self.deselectionImage = pygame.image.load("deselected.png").convert_alpha() #load the image to show that an item has been "deselected" (plain background with no red border)
        

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
                y = 34
            #if reached the end of the row, go to the next row

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
            inspectionWindow = pygame.image.load("inspection_window.png").convert() #load inspection window's image 
            
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

            if self.currentSelection.type == "armor":
                if self.currentSelection.region == "head":
                    self.image.blit(self.currentSelection.equipImage, (406, 18))
                elif self.currentSelection.region == "torso":
                    self.image.blit(self.currentSelection.equipImage, (406, 100))
                elif self.currentSelection.region == "arms":
                    self.image.blit(self.currentSelection.equipImage, (406, 182))
                elif self.currentSelection.region == "legs":
                    self.image.blit(self.currentSelection.equipImage, (407, 864))

                self.player.equipArmor(self.currentSelection)

    def selectEquipment(self, slot):
        equipmentSelected = pygame.image.load("equipment_selected.png").convert_alpha()
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
    
            
        self.equipButton.image = pygame.image.load("unequip_button.png").convert_alpha()

        self.initializeButtons()

       

    def unequip(self):

        equipmentUnselected = pygame.image.load("nothing_equipped.png").convert_alpha()
        
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

        self.equipButton.image = pygame.image.load("equip_button.png").convert_alpha()

        self.initializeButtons()

        self.currentEquipmentSelection = None


        
                    
                
        








    

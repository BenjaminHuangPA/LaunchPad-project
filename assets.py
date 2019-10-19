
import pygame



class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
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
        
        

    def move(self, x, y):
        
        #if(self.checkWallCollision() == True):
        self.walkAnim(x, y) #play the walking animation (See below)
        self.x += x #move player left/right
        self.y += y #move player right/left
        
    def walkAnim(self, x, y):
        if x < 0: #if the player walks to the left (change in x pos less than 0)
            if self.walkLeftCount < len(self.playerWalkLeftList): #loop through the list of sprites of the player walking
                leftSpriteTuple = self.playerWalkLeftList[self.walkLeftCount] #
                self.replaceBackground("left") #call blitOut2 method to blit new blank background onto the image
                self.playerWalkLeft.draw(self.image, leftSpriteTuple[0], leftSpriteTuple[1]) #call the sprite class instance's draw method to blit the correct sprite onto the image
                if self.walkLeftCount == len(self.playerWalkLeftList) - 1: 
                    self.walkLeftCount = 0 #if reached the end of the array of sprites, start over at the beginning
                else:
                    self.walkLeftCount += 1 #else, go to the next sprite
        
        if x > 0: #handle walking right
            if self.walkRightCount < len(self.playerWalkRightList):
                rightSpriteTuple = self.playerWalkRightList[self.walkRightCount]
                self.replaceBackground("right")
                self.playerWalkRight.draw(self.image, rightSpriteTuple[0], rightSpriteTuple[1])
                if self.walkRightCount == len(self.playerWalkRightList) - 1:
                    self.walkRightCount = 0
                else:
                    
                    self.walkRightCount += 1
        if y > 0:
            if self.walkBackwardCount < len(self.playerWalkBackwardList):
                downSpriteTuple = self.playerWalkBackwardList[self.walkBackwardCount]
                self.replaceBackground("down")
                self.playerWalkBackward.draw(self.image, downSpriteTuple[0], downSpriteTuple[1])
                if self.walkBackwardCount == len(self.playerWalkBackwardList) - 1:
                    self.walkBackwardCount = 0
                else:
                    self.walkBackwardCount += 1
        if y < 0:
            if self.walkForwardCount < len(self.playerWalkForwardList):
                upSpriteTuple = self.playerWalkForwardList[self.walkForwardCount]
                self.replaceBackground("up")
                self.playerWalkForward.draw(self.image, upSpriteTuple[0], upSpriteTuple[1])
                if self.walkForwardCount == len(self.playerWalkForwardList) - 1:
                    self.walkForwardCount = 0
                else:
                    self.walkForwardCount += 1
        #pygame.display.update()

        
    def update(self):
        self.rect.x = self.x * 1
        self.rect.y = self.y * 1

    

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
    def __init__ (self, game, x, y, orientation):
        self.groups = game.doors
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image = pygame.image.load("bg1.png").convert()

        self.rect = self.image.get_rect()

        self.x = x

        self.y = y

        self.orientation = orientation #denotes if the door is "forward", "backward", "left", or "right"

        self.rect.x = x * 64

        self.rect.y = y * 64

class Room(object):
    def __init__(self, game, base, door, background):
        self.base = base
        self.door = door #list of doors that this room has
        self.game = game 

        self.background = background #filename of the background image for this room's tiles

        self.doors = door

        rows, cols = (8, 8)

        #initialize array the manual way
        self.tiles = [[0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0], [0, 0, 0, 0, 0, 0, 0 ,0]]

        

        x1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        y1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for x in range(0, 8):
            for y in range(0, 8):
                self.tiles[x][y] = Tile(self.game, x1[x], x1[y], background) #fill the 2d array with tile objects 

        
#

                
        








    

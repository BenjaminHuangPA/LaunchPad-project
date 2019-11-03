
import pygame



class Player(pygame.sprite.Sprite):
    
    def __init__(self, game, x, y, inventory, HP, maxHP, STM, maxSTM, STR, AGL, INT, DEX, GRD, headArmor, torsoArmor, armArmor, legArmor, lWeapon, rWeapon):
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

        self.lWeapon = lWeapon

        self.rWeapon = rWeapon

        self.background = pygame.image.load("chasm_01_full.png").convert() #load full background image

        

    def move(self, x, y):
        
        #if(self.checkWallCollision() == True):
        self.walkAnim(x, y) #play the walking animation (See below)
        self.x += x #move player left/right
        self.y += y #move player right/left



    def takeDamage(self, DMG):
        self.HP = self.HP - DMG

    def heal(self, HP):
        self.HP = self.HP + HP

    def canEquip(self, item):
        flag = True
        if item.statReq["STR"] > self.STR:
            flag = "strength"
        if item.statReq["DEX"] > self.DEX:
            flag = "dexterity"
        if item.statReq["AGL"] > self.AGL:
            flag = "agility"
        if item.statReq["INT"] > self.INT:
            flag = "intelligence"
        if(flag == True):
            print("all good!")
        
        return flag
        
    
        
    def equipArmor(self, armor):
        if armor.region == "head":
            self.headArmor = armor
        elif armor.region == "torso":
            self.torsoArmor = armor
        elif armor.region == "arms":
            self.armArmor = armor
        elif armor.region == "legs":
            self.legArmor = armor
        self.game.callUpdateStatusBar()

    def equipWeapon(self, weapon):
        if weapon.hand == "left":
            self.lWeapon = weapon
        elif weapon.hand == "right":
            self.rWeapon = weapon
            

    def unequipArmor(self, region):
        if region == "head":
            self.headArmor = None
        elif region == "torso":
            self.torsoArmor = None
        elif region == "arms":
            self.armArmor = None
        elif region == "legs":
            self.legArmor = None
        self.game.callUpdateStatusBar()


    def unequipWeapon(self, hand):
        if hand == "lweapon":
            self.lWeapon = None
        elif hand == "rweapon":
            self.rWeapon = None

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

    def getElemATTKLeft(self):
        if self.lWeapon == None:
            empty = [0, 0, 0, 0]
            return empty
        else:
            light = self.lWeapon.elemBonus["LIGHT"]
            dark = self.lWeapon.elemBonus["DARK"]
            fire = self.lWeapon.elemBonus["FIRE"]
            ice = self.lWeapon.elemBonus["ICE"]
            elemATTKLeftArray = [light, dark, fire, ice]
            return elemATTKLeftArray

    def getElemATTKRight(self):
        if self.rWeapon == None:
            empty = [0, 0, 0, 0]
            return empty
        else:
            light = self.rWeapon.elemBonus["LIGHT"]
            dark = self.rWeapon.elemBonus["DARK"]
            fire = self.rWeapon.elemBonus["FIRE"]
            ice = self.rWeapon.elemBonus["ICE"]
            elemATTKRightArray = [light, dark, fire, ice]
            return elemATTKRightArray
        
        
    def walkAnim(self, x, y):
        if x < 0: #if the player walks to the left (change in x pos less than 0)
            if self.walkLeftCount < len(self.playerWalkLeftList): #loop through the list of sprites of the player walking
                leftSpriteTuple = self.playerWalkLeftList[self.walkLeftCount] #
                self.replaceBackground("left") #call blitOut2 method to blit new blank background onto the image
                self.playerWalkLeft.draw(self.image, leftSpriteTuple[0], leftSpriteTuple[1]) #call the sprite class instance's draw method to blit the correct sprite onto the image
                self.renderEquipment("left", leftSpriteTuple[0], leftSpriteTuple[1])
                if self.walkLeftCount == len(self.playerWalkLeftList) - 1: 
                    self.walkLeftCount = 0 #if reached the end of the array of sprites, start over at the beginning
                else:
                    self.walkLeftCount += 1 #else, go to the next sprite
        
        if x > 0: #handle walking right
            if self.walkRightCount < len(self.playerWalkRightList):
                rightSpriteTuple = self.playerWalkRightList[self.walkRightCount]
                self.replaceBackground("right")
                self.playerWalkRight.draw(self.image, rightSpriteTuple[0], rightSpriteTuple[1])
                self.renderEquipment("right", rightSpriteTuple[0], rightSpriteTuple[1])
                if self.walkRightCount == len(self.playerWalkRightList) - 1:
                    self.walkRightCount = 0
                else:
                    
                    self.walkRightCount += 1
        if y > 0:
            if self.walkBackwardCount < len(self.playerWalkBackwardList):
                downSpriteTuple = self.playerWalkBackwardList[self.walkBackwardCount]
                self.replaceBackground("down")
                self.playerWalkBackward.draw(self.image, downSpriteTuple[0], downSpriteTuple[1])
                self.renderEquipment("down", downSpriteTuple[0], downSpriteTuple[1])
                if self.walkBackwardCount == len(self.playerWalkBackwardList) - 1:
                    self.walkBackwardCount = 0
                else:
                    self.walkBackwardCount += 1
        if y < 0:
            if self.walkForwardCount < len(self.playerWalkForwardList):
                upSpriteTuple = self.playerWalkForwardList[self.walkForwardCount]
                self.replaceBackground("up")
                self.playerWalkForward.draw(self.image, upSpriteTuple[0], upSpriteTuple[1])
                self.renderEquipment("up", upSpriteTuple[0], upSpriteTuple[1])
                if self.walkForwardCount == len(self.playerWalkForwardList) - 1:
                    self.walkForwardCount = 0
                else:
                    self.walkForwardCount += 1
        #pygame.display.update()

        
    def update(self):
        self.rect.x = self.x * 1
        self.rect.y = self.y * 1

    def renderEquipment(self, direction, tuple1, tuple2):
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

        if self.lWeapon != None:
            if direction == "left":
                self.lWeapon.animWalkLeft.draw(self.image, tuple1, tuple2)
            elif direction == "right":
                self.lWeapon.animWalkRight.draw(self.image, tuple1, tuple2)
            elif direction == "down":
                self.lWeapon.animWalkBackward.draw(self.image, tuple1, tuple2)
            elif direction == "up":
                self.lWeapon.animWalkForward.draw(self.image, tuple1, tuple2)
            else:
                pass

        if self.rWeapon != None:
            if direction == "left":
                self.rWeapon.animWalkLeft.draw(self.image, tuple1, tuple2)
            elif direction == "right":
                self.rWeapon.animWalkRight.draw(self.image, tuple1, tuple2)
            elif direction == "down":
                self.rWeapon.animWalkBackward.draw(self.image, tuple1, tuple2)
            elif direction == "up":
                self.rWeapon.animWalkForward.draw(self.image, tuple1, tuple2)
            else:
                pass

        
    

    def replaceBackground(self, direction):
        

        #all of the coordinates are offset because the main game map is centered in the screen
        if direction == "right":
            self.image.blit(self.background, (0, 0), (self.x - 54, self.y - 64, 64, 64)) #get the section of background where the player is and blit it onto the image
        elif direction == "left":
            self.image.blit(self.background, (0, 0), (self.x - 74, self.y - 64, 64, 64)) #get the section of background where hte player is and blit it onto the image
        elif direction == "down":
            self.image.blit(self.background, (0, 0), (self.x - 64, self.y - 54, 64, 64))
        elif direction == "up":
            self.image.blit(self.background, (0, 0), (self.x - 64, self.y - 74, 64, 64))

    def dropItem(self, item):
        print("item dropped")
        self.game.droppedItems(item)
        self.inventory.remove(item)

    def pickUpItem(self, item):
        print("item picked up")
        



class Enemy(pygame.sprite.Sprite): #create enemy class

    def __init__(self, game, player, x, y, speed, name, HP, classification, image, forwardSpriteSheetName, backwardSpriteSheetName, leftSpriteSheetName, rightSpriteSheetName):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.player = player

        self.x = x

        self.y = y

        self.name = name

        self.HP = HP

        self.classification = classification

        self.image = pygame.image.load(image).convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x

        self.rect.y = y

        self.speed = speed

        self.enemyWalkForward = spriteSheet(forwardSpriteSheetName, 6, 1)

        self.enemyWalkForwardList = self.enemyWalkForward.getSpriteList()

        self.walkForwardCount = 0

        self.enemyWalkBackward = spriteSheet(backwardSpriteSheetName, 6, 1)

        self.enemyWalkBackwardList = self.enemyWalkBackward.getSpriteList()

        self.walkBackwardCount = 0

        self.enemyWalkLeft = spriteSheet(leftSpriteSheetName, 8, 1)

        self.enemyWalkLeftList = self.enemyWalkLeft.getSpriteList()

        self.walkLeftCount = 0

        self.enemyWalkRight = spriteSheet(rightSpriteSheetName, 8, 1)

        self.enemyWalkRightList = self.enemyWalkRight.getSpriteList()

        self.walkRightCount = 0

        self.background = pygame.image.load("chasm_01_full.png").convert() #load full background image
        


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
    def __init__(self, game, name, x, y, elemBonus, statReq, region, forwardSpriteSheetName, backwardSpriteSheetName, leftSpriteSheetName, rightSpriteSheetName, itemImage, equipImage, value, description):
        super().__init__(game, name, x, y, statReq, forwardSpriteSheetName, backwardSpriteSheetName, leftSpriteSheetName, rightSpriteSheetName, itemImage, equipImage, value, description)
        self.elemBonus = elemBonus
        self.region = region
        
class Weapon(Equipable):

    def __init__(self, game, name, x, y, weaponType, hand, weighting, dmgType, rawDMG, critChance, elemBonus, statReq, bonus, specAttack, forwardSpriteSheetName, backwardSpriteSheetName, leftSpriteSheetName, rightSpriteSheetName, itemImage, equipImage, value, description):
        super().__init__(game, name, x, y, statReq, forwardSpriteSheetName, backwardSpriteSheetName, leftSpriteSheetName, rightSpriteSheetName, itemImage, equipImage, value, description)    
        self.weaponType = weaponType
        self.hand = hand
        self.weighting = weighting
        self.dmgType = dmgType
        self.rawDMg = rawDMG
        self.critChance = critChance
        self.elemBonus = elemBonus
        self.bonus = bonus
        self.specAttack = specAttack
        self.type = "weapon"
        
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
    def __init__(self, game, base, door, background, full_background, props, enemies):
        self.base = base
        self.door = door #list of doors that this room has
        self.game = game 

        self.background = background #filename of the background image for this room's tiles

        self.full_background = full_background

        self.full_background_image = pygame.image.load(self.full_background).convert_alpha()

        self.doors = door

        rows, cols = (8, 8)

        self.props = props

        self.enemies = enemies

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

        self.rect.x = x

        self.rect.y = y

class Prop(pygame.sprite.Sprite): #props are just background images, like tables or chairs
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

    def updateBonuses(self):
        pygame.font.init()

        font1 = pygame.font.SysFont("Times New Roman", 12)\

        blank = pygame.image.load("blank_bonus.png").convert_alpha()
        
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

class enemyStatusBar(pygame.sprite.Sprite):
    def __init__(self, game, enemy, x, y):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.enemy = enemy

        self.x = x

        self.y = y

        self.image = pygame.image.load("enemy_status_bar.png").convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x

        self.rect.y = y

        self.initializeHealthBar()

    def initializeHealthBar(self):
        healthBarLength = self.enemy.HP / 3
        healthBarRect = pygame.Rect(176, 62, healthBarLength, 11)
        pygame.draw.rect(self.image, (141, 42, 42), healthBarRect)

    def initializeText(self):
        pygame.font.init()
        name = self.enemy.name

        classification = self.enemy.classification

        nameFont = pygame.font.SysFont("Times New Roman", 30)

        nameText = nameFont.render(name, False, (255, 255, 255))

        self.image.blit(nameText, (110, 13))

        classFont = pygame.font.SysFont("Times New Roman", 20)

        classText = classFont.render(classification, False, (255, 255, 255))

        self.image.blit(classText, (110, 36))


class Battle(pygame.sprite.Sprite):

    def __init__(self, game, player, enemy, x, y):
        self.groups = game.all_sprites

        pygame.sprite.Sprite.__init__(self, self.groups)

        
        self.game = game

        self.player = player

        self.enemy = enemy

        self.image = pygame.image.load("battle_screen.png").convert_alpha()

        self.x = x

        self.y = x

        self.rect = self.image.get_rect()

        self.rect.x = x

        self.rect.y = y

    def fight(self):
        while(self.enemy.HP
        
                         
        


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
            
        
class messageBox(pygame.sprite.Sprite): #simple class for displayed closeable messages to the player
    def __init__(self, game, player, x, y, message):


        self.groups = game.active_message_boxes

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.game.message_box_active = True

        self.player = player

        self.x = x

        self.y = y

        self.message = message

        self.image = pygame.image.load("message_box.png").convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x * 1

        self.rect.y = y * 1

        self.okButton = Button(self.game, 141, 113, "OK", "ok_button.png", 64, 128)

        self.image.blit(self.okButton.image, (self.okButton.x, self.okButton.y))

        textwrapper = textWrapper()

        textwrapper.blitText(self.image, 58, 28, message, 296, 22, 20, (255, 255, 255))
    
class optionBox(pygame.sprite.Sprite):
    def __init__(self, game, x, y, player, messages, mainMessage):
        self.groups = game.active_option_boxes

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game

        self.player = player

        self.messages = messages

        self.mainMessage = mainMessage

        self.x = x

        self.y = y

        self.messages = messages

        self.image = pygame.image.load("dialog_box.png").convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = x

        self.rect.y = y

        self.buttons = []
        
        self.initialize()
        

    def initialize(self):

        pygame.font.init()

        textwrapper = textWrapper()

        
        if self.messages[1] == None and self.messages[2] == None and self.messages[3] == None: #only one choice
            self.button1 = Button(self.game, 219, 76, "Message 1", "blank_button.png", 0, 0)
            self.buttons = [self.button1]
             
        elif self.messages[2] == None and self.messages[3] == None: #two choices
            self.button1 = Button(self.game, 158, 77, "Message 1", "blank_button.png", 0, 0)
            self.button2 = Button(self.game, 280, 77, "Message 2", "blank_button.png", 0, 0)
            self.buttons = [self.button1, self.button2]
            
        elif self.messages[3] == None:
            self.button1 = Button(self.game, 97, 77, "Message 1", "blank_button.png", 0, 0)
            self.button2 = Button(self.game, 219, 77, "Message 2", "blank_button.png", 0, 0)
            self.button3 = Button(self.game, 341, 77, "Message 3", "blank_button.png", 0, 0)
            self.buttons = [self.button1, self.button2, self.button3]
            
        else:
            self.button1 = Button(self.game, 73, 77, "Message 1", "blank_button.png", 0, 0)
            self.button2 = Button(self.game, 171, 77, "Message 2", "blank_button.png", 0, 0)
            self.button3 = Button(self.game, 269, 77, "Message 3", "blank_button.png", 0, 0)
            self.button4 = Button(self.game, 367, 77, "Message 4", "blank_button.png", 0, 0)
            self.buttons = [self.button1, self.button2, self.button3, self.button4]
            
        counter = 0
        for button in self.buttons:
            textwrapper.blitText(button.image, 6, 3, self.messages[counter], 60, 15, 1, (255, 255, 255))
            self.image.blit(button.image, (button.x, button.y))
            counter += 1
        
        main_font = pygame.font.SysFont("Times New Roman", 15)
        main_message_text = main_font.render(self.mainMessage, False, (255, 255, 255))
        self.image.blit(main_message_text, (46, 30))

    def checkClicked(self, x, y):
        offsetX = x - self.x
        offsetY = y - self.y
        print(offsetX)
        print(offsetY)
        for button in self.buttons:
            print(button.rect)
            if button.rect.collidepoint(offsetX, offsetY) == True:
                print("True")
                return(self.buttons.index(button) + 1)

    #def functions(self, function, *args):
    #    if function == "Pick up":
            
            
            
        

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
            if self.player.canEquip(self.currentSelection) == True:
                if self.currentSelection.type == "armor":
                    if self.currentSelection.region == "head":
                        self.image.blit(self.currentSelection.equipImage, (406, 18))
                        print("Helmet equipped!")
                    elif self.currentSelection.region == "torso":
                        self.image.blit(self.currentSelection.equipImage, (406, 100))
                        print("Chestplate equipped!")
                    elif self.currentSelection.region == "arms":
                        self.image.blit(self.currentSelection.equipImage, (406, 182))
                        print("Gauntlets equipped!")
                    elif self.currentSelection.region == "legs":
                        self.image.blit(self.currentSelection.equipImage, (407, 264))
                        print("Greaves equipped!")
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
        blank_inventory = pygame.image.load("blank_inventory.png").convert_alpha()
        self.image.blit(blank_inventory, (22, 20))
        self.fill()
            
                
                

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
        elif slot == "lweapon" and self.player.lWeapon != None:
            self.image.blit(equipmentSelected, (318, 100))
            self.currentEquipmentSelection = "lweapon"
        elif slot == "rweapon" and self.player.rWeapon != None:
            self.image.blit(equipmentSelected, (319, 182))
            self.currentEquipmentSelection = "rweapon"
            
        self.equipButton.image = pygame.image.load("unequip_button.png").convert_alpha()

        self.initializeButtons()

       

    def unequip(self):
        print("unequip method run")
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
        elif self.currentEquipmentSelection == "lweapon":
            self.player.unequipWeapon("lweapon")
            self.image.blit(equipmentUnselected, (318, 100))
        elif self.currentEquipmentSelection == "rweapon":
            self.player.unequipWeapon("rweapon")
            self.image.blit(equipmentUnselected, (318, 182))
            

        self.equipButton.image = pygame.image.load("equip_button.png").convert_alpha()

        self.initializeButtons()

        self.currentEquipmentSelection = None


        
                    
                
        








    

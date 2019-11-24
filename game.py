import pygame
import sys
from assets import *
#import objects


class Game(object):

    def __init__(self):
        pygame.init() #start up pygame
        self.window = pygame.display.set_mode((640, 790)) #set window size to 512, 512
        pygame.display.set_caption("Search") #title window
        pygame.key.set_repeat(1, 80)
        import objects

        self.all_sprites = pygame.sprite.Group()
        self.all_tiles = pygame.sprite.Group()
        self.active_tiles = pygame.sprite.Group()
        self.inventoryWindow = pygame.sprite.Group() #create a sprite group for the inventory window
        self.doors = pygame.sprite.Group()
        self.active_doors = pygame.sprite.Group() #make sprite group for this room's doors that Horace can walk through
        self.inactive_doors = pygame.sprite.Group() #make sprite group for this room's doors that are closed so that they will change appearance but still be drawn (removing them
        #from self.active_doors won't actually cause them to disappear)
        self.status_bar = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()
        self.props = pygame.sprite.Group()
        self.active_props = pygame.sprite.Group()
        self.active_message_boxes = pygame.sprite.Group() #sprite group to hold active message boxes
        self.active_option_boxes = pygame.sprite.Group()
        self.active_enemies = pygame.sprite.Group()
        self.title_screen = pygame.sprite.Group()

        self.active_ground_items = pygame.sprite.Group()

        self.message_box_active = False #check if there are active message boxes

        self.active_battle = pygame.sprite.Group()
        self.active_enemy_status_bar = pygame.sprite.Group()

        #for prop in objects.cave_plants:
        #    self.props.add(prop)

        

        self.clock = pygame.time.Clock()

        apple = item(self, 91, 91, "img/items/misc/apple_2.png", 'Apple', 2, 'Here is an unnecessarily long description of an apple. It is entirely to test the function of the textWrapper class', True, 'common', 1)
        apple2 = item(self, 64, 64, "img/items/misc/apple_2.png", 'Apple', 2, 'Another apple', True, 'common', 1)
        apple3 = item(self, 64, 64, "img/items/misc/apple_2.png", 'Apple', 2, 'A third apple', True, 'common', 1)


        broken_gauntlets_statreq = {"STR": 1, "DEX": 0, "AGL": 0, "INT": 0}

        broken_cuirass_statreq = {"STR": 2, "DEX": 0, "AGL": 0, "INT": 0}

        broken_gauntlets_elembonus = {"LIGHT": 12, "DARK": 0, "FIRE": 0, "ICE": 0}

        broken_cuirass_elembonus = {"LIGHT": 2, "DARK": 3, "FIRE": 0, "ICE": 0}

        broken_greaves_statreq = {"STR": 0, "DEX": 0, "AGL": 0, "INT": 0}

        broken_greaves_elembonus = {"LIGHT": 0, "DARK": 0, "FIRE": 0, "ICE": 0}

        cracked_helmet_elembonus = {"LIGHT": 12, "DARK": 0, "FIRE": 0, "ICE": 0}

        cracked_helmet_statreq = {"STR": 0, "DEX": 0, "AGL": 0, "INT": 0}

        self.broken_gauntlets = Armor(self, "Broken gauntlets", 64, 64, broken_gauntlets_elembonus, broken_gauntlets_statreq, "arms", "broken", "gauntlets", 10, "A pair of broken gauntlets")

        self.broken_cuirass = Armor(self, "Broken cuirass", 64, 64, broken_cuirass_elembonus, broken_cuirass_statreq, "torso", "broken", "cuirass", 6, "A broken cuirass.")

        self.broken_greaves = Armor(self, "Broken greaves", 64, 64, broken_greaves_elembonus, broken_greaves_statreq, "legs", "broken", "greaves", 8, "A pair of broken greaves.")

        self.cracked_helmet = Armor(self, "Cracked helmet", 64, 64, cracked_helmet_elembonus, cracked_helmet_statreq, "head", "broken", "helmet", 8, "A cracked helmet.")
        
        broken_sword_statreq = {"STR": 2, "DEX": 0, "AGL": 0, "INT": 0}

        broken_sword_elembonus = {"LIGHT": 0, "DARK": 0, "FIRE": 0, "ICE": 0}

        self.broken_sword = Weapon(self, "Broken sword", 64, 64, "Straight sword", "right", "medium", "piercing", 8, 8, broken_sword_elembonus, broken_sword_statreq, None, None, "broken_sword", 15, "Horace's guardsman's sword. Mostly ornamental, its blade is now broken in two by falling rubble.")

        inventory = [apple, apple2, apple3, self.broken_gauntlets, self.broken_cuirass, self.broken_greaves, self.cracked_helmet, self.broken_sword] #create very basic inventory array
        
        self.player = Player(self, 64, 64, inventory, 50, 50, 20, 20, 3, 5, 5, 3, 5, None, None, None, None, None, None)

        self.goblin = Enemy(self, self.player, 384, 384, 2, "Goblin", 20, 20, None, None, None, None, "Beast", "goblin")

        self.goblin_2 = Enemy(self, self.player, 256, 384, 2, "Goblin", 20, 20, None, None, None, None, "Beast", "goblin")


        room_1_enemies = [self.goblin, self.goblin_2]
        

        self.rightDoor = Door(self, 9, 4, "right", True, "img/tile/chasm/chasm_door_right.png", "img/tile/chasm/chasm_wall_right.png" ) #initialize doors. There will be only four doors, each representing a cardinal direction. A room can have 1-4 doors.
        self.leftDoor = Door(self, 0, 4, "left", True, "img/tile/chasm/chasm_door_left.png", "img/tile/chasm/chasm_wall_left.png")
        self.forwardDoor = Door(self, 4, 0, "forward", True, "img/tile/chasm/chasm_door_top.png", "img/tile/chasm/chasm_wall_top.png")
        self.backwardDoor = Door(self, 4, 9, "backward", True, "img/tile/chasm/chasm_door_bottom.png", "img/tile/chasm/chasm_wall_top.png")
        
        self.display_inventory = False #flag to check whether the inventory window is open or not
        
        self.z1r1 = Room(self, "base", [self.backwardDoor], "img/tile/chasm/chasm_01.png", "img/tile/chasm/chasm_01_full.png", objects.props_z1r1, room_1_enemies) #initialize some basic rooms, each with a different background image to tell them apart.
        #enter a list of doors to represent the doors of the room.
        self.z2r2 = Room(self, "base", [self.backwardDoor, self.forwardDoor, self.rightDoor], "img/tile/chasm/chasm_01.png", "img/tile/chasm/chasm_01_full.png", objects.props_z1r2, [])
        self.z3r3 = Room(self, "base", [self.forwardDoor], "img/tile/chasm/chasm_01.png", "img/tile/chasm/chasm_01_full.png", objects.props_z1r3, [])
        self.z4r4 = Room(self, "base", [self.leftDoor], "img/tile/chasm/chasm_01.png", "img/tile/chasm/chasm_01_full.png", objects.props_z1r4, [])
        
        self.ZONE1 = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, self.z1r1, 0, 0, 0, 0], [0, self.z2r2, self.z4r4, 0, 0, 0], [0, self.z3r3, 0, 0, 0, 0]]

        self.battle = False

        self.titlescreen = TitleScreen(self, 0, 0)

        self.clock_group = pygame.sprite.Group()


        #create a 2D array of rooms to represent this zone.

        #self.currentLocation = 

        #self.z1r1 = Room(self, "base", "door", "img/tile/chasm/chasm_01.png") #create a new Room object (see assets.py)
        #for x in range(0, 8):
        #    for y in range(0, 8):
        #        self.active_tiles.add(self.z1r1.tiles[x][y])
                #fill the active_tiles sprite group with the tiles from the room object

        #create some random items
        
        
        #messages = ["Yes", "No", None, None]
        #dialogBox = optionBox(self, 64, 512, self.player, messages, "Will you accept the blessing?")
        #dialogBox.add(self.active_option_boxes)
         

        pygame.font.init()

        self.clock = pygame.time.Clock()

        self.prevKey = None

    def new(self):

        
        self.leftwall = pygame.image.load("img/tile/chasm/chasm_wall_left.png").convert()
        self.rightwall = pygame.image.load("img/tile/chasm/chasm_wall_right.png").convert()
        self.topwall = pygame.image.load("img/tile/chasm/chasm_wall_top.png").convert()
        self.bottomwall = pygame.image.load("img/tile/chasm/chasm_wall_bottom.png").convert()

        self.window.blit(self.rightwall, (576, 0))

        self.window.blit(self.topwall, (0, 0))

        self.window.blit(self.bottomwall, (0, 576))

        self.window.blit(self.leftwall, (0, 0))
        

        self.statusbar = statusBar(self, self.player, 0, 640)

        self.statusbar.updateBonuses()

        self.startingRoom = self.ZONE1[self.player.roomLocation[0]][self.player.roomLocation[1]] #access the 2D array "ZONE1" above and get the room that the player starts in

        self.activeRoom = 0 #initialize the active room to 0 (will later be a room object)
        
        #self.z1r1 = Room(self, "base", "door", "img/tile/chasm/chasm_01.png") #create a new Room object (see assets.py)
        for x in range(0, 8):
            for y in range(0, 8):
                self.active_tiles.add(self.startingRoom.tiles[x][y])
                #fill the active_tiles sprite group with the tiles from the room object        
        for door in self.startingRoom.doors:
            self.active_doors.add(door)

        self.inventory = inventoryGUI(self, self.player, 64, 128) #initialize new inventoryGUI object (see assets.py)


    def titleScreen(self):
        self.title = True
        
        while self.title == True:
            self.titleScreenEvents()
            self.titleScreenDraw()
            self.titleScreenUpdate()


    def titleScreenDraw(self):
        self.title_screen.draw(self.window)

    def titleScreenUpdate(self):
        self.title_screen.update()
    

    def run(self): #method to run the game
        self.playing = True #initialize "self.playing" to true
        while self.playing == True:
            #pygame.time.delay(100) #while self.playing == true, delay + run self.events()
            if self.battle == False:
                self.events() #call the events method below
            else:
                self.battleEvents()
            if self.battle == False:
                self.move_enemies()

            self.draw() #call the draw method below
            #if self.battle == True:
            #    self.battleEvent.add(self.active_battle)
                
            
            self.update()
            self.clock.tick(25)

    def titleScreenEvents(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.title = False
            
            if event.type == pygame.MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()

                self.titlescreen.buttonMouseOver(mousePos)

            if event.type == pygame.MOUSEBUTTONDOWN:

                mousePos = pygame.mouse.get_pos()

                if self.titlescreen.clickButton(mousePos) == 4:
                    self.quit()
                elif self.titlescreen.clickButton(mousePos) == 1:
                    self.title = False

            
            
        pygame.display.flip()
                
                
                
                
            
            
    def events(self):
        for event in pygame.event.get(): #loop through events of pygame
            
            if event.type == pygame.QUIT: 
                self.quit() #if the event is "quit" run the method self.quit()
            if event.type == pygame.KEYDOWN:

                
                
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_LEFT and self.player.x > 64 and self.checkPropCollisions("left") == False:
                    self.player.move(-10, 0)
                    self.prevKey = "l"
               
                    
                if event.key == pygame.K_RIGHT and self.player.x < 512 and self.checkPropCollisions("right") == False:
                    self.player.move(10, 0)
                    self.prevKey = "r"

                        
                if event.key == pygame.K_UP and self.player.y > 64 and self.checkPropCollisions("up") == False:
                    self.player.move(0, -10)
                    self.prevKey = "u"
                    
                if event.key == pygame.K_DOWN and self.player.y < 512 and self.checkPropCollisions("down") == False:
                    self.player.move(0, 10)
                    self.prevKey = "d"
                
                if event.key == pygame.K_e:
                    
                    if self.display_inventory == True:
                        self.display_inventory = False
                        self.toggleInventoryVisibility()
                    elif self.display_inventory == False:
                        self.display_inventory = True
                        self.toggleInventoryVisibility()

                if event.key == pygame.K_d:
                    self.player.takeDamage(1)
                    self.statusbar.decreaseHealth(1)

                if event.key == pygame.K_h:
                    self.player.heal(1)
                    self.statusbar.increaseHealth(1)

            if event.type == pygame.KEYUP:
                if self.prevKey == "l" or self.prevKey == "r" or self.prevKey == "u" or self.prevKey == "d":
                    self.player.idle()        
                
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos() #get position of mouse on the screen
                
                #print(self.display_inventory)
                #print(self.inventory.dropButton.rect)
                
                if(self.display_inventory == True): #only process this loop if the inventory is visible on the screen
                    headRect = pygame.Rect(470, 146, 64, 64)
                    torsoRect = pygame.Rect(470, 228, 64, 64)
                    armsRect = pygame.Rect(470, 310, 64, 64)
                    legsRect = pygame.Rect(470, 392, 64, 64)
                    lWeaponRect = pygame.Rect(382, 228, 64, 64)
                    rWeaponRect = pygame.Rect(383, 310, 64, 64)

                    if self.inventory.dropButton.rect.collidepoint(mousePos) == True: #check if drop button clicked
                        self.inventory.drop()
                        print("Drop button clicked!")
                    elif self.inventory.equipButton.rect.collidepoint(mousePos) == True: #check if equip button clicked
                        print("Equip button clicked!")
                        if(self.inventory.currentEquipmentSelection == None):
                            self.inventory.equip()
                        else:
                            self.inventory.unequip()
                    elif self.inventory.inspectButton.rect.collidepoint(mousePos) == True: #check if inspect button clicked
                        self.inventory.inspect() #run inventoryGUI's inspect() function
                        
                    elif self.inventory.sellButton.rect.collidepoint(mousePos) == True: #check if sell button clicked
                        print("Sell button clicked!")
                    elif headRect.collidepoint(mousePos) == True:
                        self.inventory.selectEquipment("head")
                    elif torsoRect.collidepoint(mousePos) == True:
                        self.inventory.selectEquipment("torso")
                    elif armsRect.collidepoint(mousePos) == True:
                        self.inventory.selectEquipment("arms")
                    elif legsRect.collidepoint(mousePos) == True:
                        self.inventory.selectEquipment("legs")
                    elif lWeaponRect.collidepoint(mousePos) == True:
                        self.inventory.selectEquipment("lweapon")
                    elif rWeaponRect.collidepoint(mousePos) == True:
                        self.inventory.selectEquipment("rweapon")
                    for item in self.player.inventory:
                        offsetRect = pygame.Rect((item.x + 64, item.y + 128), (item.rect.x, item.rect.y)) 
                        #for each item in the player's inventory, create an offset rectangle (because the inventory window's
                        #top left point is not at the game window's (0,0)
                        if offsetRect.collidepoint(mousePos) == True: #check if an item was clicked
                            print("wtf?")
                            self.inventory.select(item) #run method defined in inventoryGUI class body (see assets.py)

                if self.message_box_active == True:
                    mousePos = pygame.mouse.get_pos()
                    for sprite in self.active_message_boxes.sprites():
                        if sprite.okButton.rect.collidepoint(mousePos) == True:
                            sprite.remove(self.active_message_boxes)
                for optionBox in self.active_option_boxes:
                    print(optionBox.checkClicked(mousePos[0], mousePos[1]))
                        
                    
            self.checkCollisions()
            self.checkItemCollisions()
            self.checkEnemyCollisions()
            
        pygame.display.flip()

    def battleEvents(self):
        CLOCK_TICK = pygame.USEREVENT
        #pygame.time.set_timer(CLOCK_TICK, 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    pygame.time.set_timer(CLOCK_TICK, 1000)
                else:
                    self.battleEvent.game_clock.tick()
                    time_elapsed = self.battleEvent.game_clock.get_time()
                    if event.key == pygame.K_UP:
                        key_up = ("UP", time_elapsed)
                        self.battleEvent.keyInputHandler(key_up)
                    elif event.key == pygame.K_DOWN:
                        key_down = ("DOWN", time_elapsed)
                        self.battleEvent.keyInputHandler(key_down)
                    elif event.key == pygame.K_LEFT:
                        key_left = ("LEFT", time_elapsed)
                        self.battleEvent.keyInputHandler(key_left)
                    elif event.key == pygame.K_RIGHT:
                        key_right = ("RIGHT", time_elapsed)
                        self.battleEvent.keyInputHandler(key_right)
                        
                
            if event.type == CLOCK_TICK:
                    print("Clock ticked!")
                    
                    self.battleEvent.turn_determiner()
            
                
            
                    
    def quit(self):
        pygame.quit() #quit pygame
        sys.exit() #close (IDLE is kind of weird with this)

    def draw_grid(self):
        for x in range(0, 512, 64): #every 64 pixels from 0 to 512 (window border):
            pygame.draw.line(self.window, (100, 100, 100), (x, 0), (x, 512))
            #draw a light grey line on the window from each x to the bottom of the screen
        for y in range(0, 512, 64): #every 64 pixels from 0 to 512 (window border):
            pygame.draw.line(self.window, (100, 100, 100), (0, y), (512, y))
            #draw a light grey line on the window from each y to the right of the screen.

    def move_enemies(self):
        for enemy in self.active_enemies.sprites():
            enemy.move()

    def droppedItems(self, item):

        print("method run!")
        print(self.player.x)
        print(self.player.y)
        item.x = self.player.x - 20
        item.y = self.player.y + 30
        item.rect.x = item.x
        item.rect.y = item.y
        print(item.x)
        print(item.y)
        item.add(self.active_ground_items)


    def draw(self):
       
       
       self.draw_grid() #call the draw_grid method

       self.status_bar.draw(self.window)


       
       self.active_tiles.draw(self.window) #draw all tiles in the active_tiles group
       self.active_doors.draw(self.window)
       self.inactive_doors.draw(self.window)
       #group to the screen

       self.active_props.draw(self.window) #draw all of the current room's props to the screen

       self.entities.draw(self.window) #draw all entities

       self.active_enemies.draw(self.window)


       self.active_ground_items.draw(self.window)

       self.active_option_boxes.draw(self.window)


       self.inventoryWindow.draw(self.window)

       self.active_message_boxes.draw(self.window)

       self.active_battle.draw(self.window)

       self.active_enemy_status_bar.draw(self.window)

       self.clock_group.draw(self.window)

       pygame.display.flip() #update the surfaces

    def callUpdateStatusBar(self):
        self.statusbar.updateBonuses()

    def checkPropCollisions(self, direction):
        #collides = False
        #for prop in self.active_props.sprites():
        #    if pygame.sprite.collide_rect(self.player, prop) == True:
        #        collides = True

        #return collides
        collides = False
    
        for prop in self.active_props.sprites(): #this code works for some reason. I have no idea why. It just does.
            if pygame.sprite.collide_rect(self.player, prop) == True:
                if direction == "left":
                    if prop.x < self.player.x:
                        collides = True
                elif direction == "right":
                    if prop.x > self.player.x:
                        collides = True
                elif direction == "up":
                    if prop.y < self.player.y:
                        collides = True
                elif direction == "down":
                    if prop.y > self.player.y:
                        collides = True

        return collides
            
    def checkItemCollisions(self):
        hasCollided = False
        itemName = None
        for item in self.active_ground_items.sprites():
            if pygame.sprite.collide_rect(self.player, item) == True:
                itemName = item.name
                hasCollided = True
        if hasCollided == True:
            messages = ["Pick up", "Leave", None, None]
            mainMessage = "Pick up " + itemName + "?"
            if len(self.active_option_boxes.sprites()) < 1:
                pickUpItem = optionBox(self, 64, 448, self.player, messages, mainMessage)
            
        else:
            self.active_option_boxes.empty()

            
    def checkEnemyCollisions(self):
        for enemy in self.active_enemies.sprites():
            if pygame.sprite.collide_rect(self.player, enemy) == True:
                self.battle = True
                self.battleEvent = Battle(self, self.player, enemy, 0, 150)
                self.battleEvent.add(self.active_battle)
                

    def toggleInventoryVisibility(self):
        if self.display_inventory == True:
            self.inventoryWindow.add(self.inventory)
        else:
            self.inventoryWindow.remove(self.inventory)

    def update(self):
       self.all_sprites.update()
       #self.active_battle.update
       #pygame.display.flip()

    def checkCollisions(self):

        #for some clarification, the player's roomLocation variable is an array of the format [x, y] that is used to determine what room of the 2D array "ZONE1"
        # (or zone in general) the player is currently in. So if the player enters a door to the right of the room, we would increase y by one
        
       if pygame.sprite.collide_rect(self.player, self.rightDoor) == True and self.rightDoor.status == True: #check if the player entered a door on the right side of a room
          
          self.player.roomLocation[1] = self.player.roomLocation[1] + 1 #modify the player's roomLocation variable one space to the right

          print(self.player.roomLocation)

          self.switchRooms("right") #call switchRooms function below

       elif pygame.sprite.collide_rect(self.player, self.leftDoor) == True and self.leftDoor.status == True: #check if the player entered a door on the left side of a room

          self.player.roomLocation[1] = self.player.roomLocation[1] - 1 #modify the player's roomLocation variable one space to the left

          print(self.player.roomLocation)

          self.switchRooms("left") #call switchRooms function below
          
       elif pygame.sprite.collide_rect(self.player, self.forwardDoor) == True and self.forwardDoor.status == True: #check if the player entered a door that goes into a room beyond the room the player is currently in
           self.player.roomLocation[0] = self.player.roomLocation[0] - 1 #modify the player's roomLocation variable one space "up"

           print(self.player.roomLocation)

           self.switchRooms("forward") #call switchRooms function below

       elif pygame.sprite.collide_rect(self.player, self.backwardDoor) == True and self.backwardDoor.status == True: #check if the player entered a door that goes into a room behind the room the player is currently in
           self.player.roomLocation[0] = self.player.roomLocation[0] + 1

           print(self.player.roomLocation)

           self.switchRooms("backward") #call switchRooms function below

       elif pygame.sprite.collide_rect(self.player, self.rightDoor) == True and self.rightDoor.status == False:
           print("Error message")
       
    
          #for sprite in self.all_tiles.sprites():
          #    sprite.remove(self.all_tiles)
          #print(self.all_tiles.sprites())
          #for x in range(0, 8):
          #  for y in range(0, 8):
          #      self.active_tiles.add(self.z2r2.tiles[x][y])
          #print(self.active_tiles.sprites())

    def switchRooms(self, direction):
        self.activeRoom = self.ZONE1[self.player.roomLocation[0]][self.player.roomLocation[1]] #since the player's roomLocation was modified in checkCollisions(), update the activeRoom
        #variable to be the room the player has just moved to
        
        for sprite in self.active_tiles.sprites():
              sprite.remove(self.active_tiles) #remove all tiles currently in the active_tiles sprite group

        for prop in self.active_props.sprites(): #remove all of the previous room's props as well
            prop.remove(self.active_props)

        for enemy in self.active_enemies.sprites():
            enemy.remove(self.active_enemies)
        
        for x in range(0, 8):
            for y in range(0, 8):
                self.active_tiles.add(self.activeRoom.tiles[x][y]) #fill the now empty active_tiles sprite group with tiles from the new room the player has just moved to
                #these will be drawn almost instantly 
        #print(self.active_tiles.sprites())
        if direction == "right":
            self.player.x = 70 #make sure that if the player enters a door to the right, they come out on the left side of the next room
            self.player.y = 256
        elif direction == "left":
            self.player.x = 506 #make sure that if the player enters a door to the left, they come out on the right side of the next room
            self.player.y = 256
        elif direction == "forward":
            self.player.x = 256 #make sure that if the player enters a door ahead of them, they come out at the "back" (relatively speaking) of the next room
            self.player.y = 506
        elif direction == "backward":
            self.player.x = 256 #make sure that if the player enters a door that's behind them, they come out at the "front" (relatively speaking) of the next room
            self.player.y = 70
        for door in self.active_doors:
            door.closeDoor()
            door.status = False
            door.add(self.inactive_doors) #remove the previous room's doors from the door sprite group so that they will (theoretically) no longer be drawn
            
        
        for door in self.activeRoom.doors:
            door.add(self.active_doors) #add the next room's doors to the active_doors sprite group to be drawn
            door.status = True
            door.openDoor()

        for prop in self.activeRoom.props:
            prop.add(self.active_props)

        for enemy in self.activeRoom.enemies:
            enemy.add(self.active_enemies)

        self.player.background = self.activeRoom.full_background_image
            

        
          
       

g = Game() #initialize new game object
while True:
    g.clock.tick(16)
    g.titleScreen()
    g.new()
    g.run() #call run method
    

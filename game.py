import pygame
import sys
from assets import *
#import objects



class Game(object):

    def __init__(self):
        pygame.init() #start up pygame
        self.window = pygame.display.set_mode((640, 790)) #set window size to 512, 512
        pygame.display.set_caption("First game") #title window
        pygame.key.set_repeat(500, 100)
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

        #for prop in objects.cave_plants:
        #    self.props.add(prop)

        self.leftwall = pygame.image.load("chasm_wall_left.png").convert()
        self.rightwall = pygame.image.load("chasm_wall_right.png").convert()
        self.topwall = pygame.image.load("chasm_wall_top.png").convert()
        self.bottomwall = pygame.image.load("chasm_wall_bottom.png").convert()

        self.window.blit(self.rightwall, (576, 0))

        self.window.blit(self.topwall, (0, 0))

        self.window.blit(self.bottomwall, (0, 576))

        self.window.blit(self.leftwall, (0, 0))

        self.clock = pygame.time.Clock()

        self.rightDoor = Door(self, 9, 4, "right", True, "chasm_door_right.png", "chasm_wall_right.png" ) #initialize doors. There will be only four doors, each representing a cardinal direction. A room can have 1-4 doors.
        self.leftDoor = Door(self, 0, 4, "left", True, "chasm_door_left.png", "chasm_wall_left.png")
        self.forwardDoor = Door(self, 4, 0, "forward", True, "chasm_door_top.png", "chasm_wall_top.png")
        self.backwardDoor = Door(self, 4, 9, "backward", True, "chasm_door_bottom.png", "chasm_wall_top.png") 
        
        self.display_inventory = False #flag to check whether the inventory window is open or not
        
        self.z1r1 = Room(self, "base", [self.backwardDoor], "chasm_01.png", objects.props_z1r1) #initialize some basic rooms, each with a different background image to tell them apart.
        #enter a list of doors to represent the doors of the room.
        self.z2r2 = Room(self, "base", [self.backwardDoor, self.forwardDoor, self.rightDoor], "chasm_02.png", objects.props_z1r2)
        self.z3r3 = Room(self, "base", [self.forwardDoor], "chasm_03.png", objects.props_z1r3)
        self.z4r4 = Room(self, "base", [self.leftDoor], "chasm_04.png", objects.props_z1r4)
        
        self.ZONE1 = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, self.z1r1, 0, 0, 0, 0], [0, self.z2r2, self.z4r4, 0, 0, 0], [0, self.z3r3, 0, 0, 0, 0]]

        #create a 2D array of rooms to represent this zone.

        #self.currentLocation = 

        #self.z1r1 = Room(self, "base", "door", "chasm_01.png") #create a new Room object (see assets.py)
        #for x in range(0, 8):
        #    for y in range(0, 8):
        #        self.active_tiles.add(self.z1r1.tiles[x][y])
                #fill the active_tiles sprite group with the tiles from the room object

        #create some random items
        
        self.apple = item(self, 64, 64, "apple_2.png", 'Apple', 2, 'Here is an unnecessarily long description of an apple. It is entirely to test the function of the textWrapper class', True, 'common', 1)
        self.apple2 = item(self, 64, 64, "apple_2.png", 'Apple', 2, 'Another apple', True, 'common', 1)
        self.apple3 = item(self, 64, 64, "apple_2.png", 'Apple', 2, 'A third apple', True, 'common', 1)

        self.broken_gauntlets = Armor(self, "Broken gauntlets", 64, 64, "head", "broken_gauntlets_game_back.png", "broken_gauntlets_game_front.png", "broken_gauntlets_game_left.png", "broken_gauntlets_game_right.png", "broken_gauntlets_32x32.png", "broken_gauntlets_game.png", 10, "A pair of broken gauntlets")

        self.broken_cuirass = Armor(self, "Broken cuirass", 64, 64, "arms", "broken_cuirass_game_back.png", "broken_cuirass_game_front.png", "broken_cuirass_game_left.png", "broken_cuirass_game_right.png", "broken_cuirass_32x32.png", "broken_cuirass_game.png", 6, "A broken cuirass.")

        pygame.font.init()

    def new(self):

        inventory = [self.apple, self.apple2, self.apple3, self.broken_gauntlets, self.broken_cuirass] #create very basic inventory array
        
        self.player = Player(self, 64, 64, inventory, 50, 50, 20, 20, 3, 5, 5, 3, 5, None, None, None, None)

        self.statusbar = statusBar(self, self.player, 0, 640)

        self.startingRoom = self.ZONE1[self.player.roomLocation[0]][self.player.roomLocation[1]] #access the 2D array "ZONE1" above and get the room that the player starts in

        self.activeRoom = 0 #initialize the active room to 0 (will later be a room object)
        
        #self.z1r1 = Room(self, "base", "door", "chasm_01.png") #create a new Room object (see assets.py)
        for x in range(0, 8):
            for y in range(0, 8):
                self.active_tiles.add(self.startingRoom.tiles[x][y])
                #fill the active_tiles sprite group with the tiles from the room object        
        for door in self.startingRoom.doors:
            self.active_doors.add(door)

        self.inventory = inventoryGUI(self, self.player, 64, 128) #initialize new inventoryGUI object (see assets.py)

    def run(self): #method to run the game
        self.playing = True #initialize "self.playing" to true
        while self.playing == True:
            #pygame.time.delay(100) #while self.playing == true, delay + run self.events()
            self.events() #call the events method below
            self.draw() #call the draw method below
            self.update()
            
            
            
    def events(self):
        for event in pygame.event.get(): #loop through events of pygame
            if event.type == pygame.QUIT: 
                self.quit() #if the event is "quit" run the method self.quit()
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    self.quit()
                if event.key == pygame.K_LEFT and self.player.x > 64 and self.checkPropCollisions() == False:
                    self.player.move(-10, 0)
                    
                if event.key == pygame.K_RIGHT and self.player.x < 512 and self.checkPropCollisions() == False:
                    
                    self.player.move(10, 0)
                        
                if event.key == pygame.K_UP and self.player.y > 64 and self.checkPropCollisions() == False:
                    self.player.move(0, -10)
                    
                if event.key == pygame.K_DOWN and self.player.y < 512 and self.checkPropCollisions() == False:
                    self.player.move(0, 10)
                
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
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos() #get position of mouse on the screen
                
                #print(self.display_inventory)
                #print(self.inventory.dropButton.rect)
                
                if(self.display_inventory == True): #only process this loop if the inventory is visible on the screen
                    headRect = pygame.Rect(470, 146, 64, 64)
                    torsoRect = pygame.Rect(470, 228, 64, 64)
                    armsRect = pygame.Rect(470, 310, 64, 64)
                    legsRect = pygame.Rect(470, 392, 64, 64)
                    

                    if self.inventory.dropButton.rect.collidepoint(mousePos) == True: #check if drop button clicked
                        
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
                    for item in self.player.inventory:
                        offsetRect = pygame.Rect((item.x + 64, item.y + 128), (item.rect.x, item.rect.y)) 
                        #for each item in the player's inventory, create an offset rectangle (because the inventory window's
                        #top left point is not at the game window's (0,0)
                        if offsetRect.collidepoint(mousePos) == True: #check if an item was clicked
                            print("wtf?")
                            self.inventory.select(item) #run method defined in inventoryGUI class body (see assets.py)
                            
                        
                    
            self.checkCollisions()
        pygame.display.flip()
                    
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

    def draw(self):
       
       
       self.draw_grid() #call the draw_grid method

       self.status_bar.draw(self.window)
       
       self.active_tiles.draw(self.window) #draw all tiles in the active_tiles group
       self.active_doors.draw(self.window)
       self.inactive_doors.draw(self.window)
       #group to the screen

       self.active_props.draw(self.window) #draw all of the current room's props to the screen

       self.entities.draw(self.window) #draw all entities


       self.inventoryWindow.draw(self.window)

       pygame.display.flip() #update the surfaces

    def checkPropCollisions(self):
        collides = False
        for prop in self.active_props.sprites():
            if pygame.sprite.collide_rect(self.player, prop) == True:
                collides = True

        return collides

    def toggleInventoryVisibility(self):
        if self.display_inventory == True:
            self.inventoryWindow.add(self.inventory)
        else:
            self.inventoryWindow.remove(self.inventory)

    def update(self):
       self.all_sprites.update()
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
            

        
          
       

g = Game() #initialize new game object
while True:
    g.clock.tick(16)
    g.new()
    g.run() #call run method
    

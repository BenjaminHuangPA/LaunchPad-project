import pygame
import sys
from assets import *

class Game(object):

    #this is a GitHub test

    def __init__(self):
        pygame.init() #start up pygame
        self.window = pygame.display.set_mode((640, 640)) #set window size to 512, 512
        pygame.display.set_caption("First game") #title window
        pygame.key.set_repeat(500, 100)

        self.all_sprites = pygame.sprite.Group()
        self.all_tiles = pygame.sprite.Group()
        self.active_tiles = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.active_doors = pygame.sprite.Group() #make sprite group for this room's doors
        self.entities = pygame.sprite.Group()

        self.clock = pygame.time.Clock()

        self.rightDoor = Door(self, 9, 4, "right") #initialize doors. There will be only four doors, each representing a cardinal direction. A room can have 1-4 doors.
        self.leftDoor = Door(self, 0, 4, "left")
        self.forwardDoor = Door(self, 4, 0, "forward")
        self.backwardDoor = Door(self, 4, 9, "backward") 
        
        
        self.z1r1 = Room(self, "base", [self.backwardDoor], "chasm_01.png") #initialize some basic rooms, each with a different background image to tell them apart.
        #enter a list of doors to represent the doors of the room.
        self.z2r2 = Room(self, "base", [self.backwardDoor, self.forwardDoor, self.rightDoor], "chasm_02.png")
        self.z3r3 = Room(self, "base", [self.forwardDoor], "chasm_03.png")
        self.z4r4 = Room(self, "base", [self.leftDoor], "chasm_04.png")
        
        self.ZONE1 = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, self.z1r1, 0, 0, 0, 0], [0, self.z2r2, self.z4r4, 0, 0, 0], [0, self.z3r3, 0, 0, 0, 0]]

        #create a 2D array of rooms to represent this zone.

        #self.currentLocation = 

        #self.z1r1 = Room(self, "base", "door", "chasm_01.png") #create a new Room object (see assets.py)
        #for x in range(0, 8):
        #    for y in range(0, 8):
        #        self.active_tiles.add(self.z1r1.tiles[x][y])
                #fill the active_tiles sprite group with the tiles from the room object
        

    def new(self):
        
        self.player = Player(self, 64, 64)
        

        self.startingRoom = self.ZONE1[self.player.roomLocation[0]][self.player.roomLocation[1]] #access the 2D array "ZONE1" above and get the room that the player starts in

        self.activeRoom = 0 #initialize the active room to 0 (will later be a room object)
        
        #self.z1r1 = Room(self, "base", "door", "chasm_01.png") #create a new Room object (see assets.py)
        for x in range(0, 8):
            for y in range(0, 8):
                self.active_tiles.add(self.startingRoom.tiles[x][y])
                #fill the active_tiles sprite group with the tiles from the room object        
        for door in self.startingRoom.doors:
            self.active_doors.add(door)

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
                if event.key == pygame.K_LEFT and self.player.x > 64:
                    self.player.move(-10, 0)
                    
                if event.key == pygame.K_RIGHT and self.player.x < 512:
                    
                    self.player.move(10, 0)
                        
                if event.key == pygame.K_UP and self.player.y > 64:
                    self.player.move(0, -10)
                    
                if event.key == pygame.K_DOWN and self.player.y < 512:
                    self.player.move(0, 10)
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
       
       self.active_tiles.draw(self.window) #draw all tiles in the active_tiles group
       self.entities.draw(self.window) #draw all entities
       self.active_doors.draw(self.window)
       #group to the screen
       pygame.display.flip() #update the surfaces

    def update(self):
       self.all_sprites.update()
       #pygame.display.flip()

    def checkCollisions(self):

        #for some clarification, the player's roomLocation variable is an array of the format [x, y] that is used to determine what room of the 2D array "ZONE1"
        # (or zone in general) the player is currently in. So if the player enters a door to the right of the room, we would increase y by one
        
       if pygame.sprite.collide_rect(self.player, self.rightDoor) == True: #check if the player entered a door on the right side of a room
          
          self.player.roomLocation[1] = self.player.roomLocation[1] + 1 #modify the player's roomLocation variable one space to the right

          print(self.player.roomLocation)

          self.switchRooms("right") #call switchRooms function below

       elif pygame.sprite.collide_rect(self.player, self.leftDoor) == True: #check if the player entered a door on the left side of a room

          self.player.roomLocation[1] = self.player.roomLocation[1] - 1 #modify the player's roomLocation variable one space to the left

          print(self.player.roomLocation)

          self.switchRooms("left") #call switchRooms function below
          
       elif pygame.sprite.collide_rect(self.player, self.forwardDoor) == True: #check if the player entered a door that goes into a room beyond the room the player is currently in
           self.player.roomLocation[0] = self.player.roomLocation[0] - 1 #modify the player's roomLocation variable one space "up"

           print(self.player.roomLocation)

           self.switchRooms("forward") #call switchRooms function below

       elif pygame.sprite.collide_rect(self.player, self.backwardDoor) == True: #check if the player entered a door that goes into a room behind the room the player is currently in
           self.player.roomLocation[0] = self.player.roomLocation[0] + 1

           print(self.player.roomLocation)

           self.switchRooms("backward") #call switchRooms function below

    
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
            door.remove(self.active_doors) #remove the previous room's doors from the door sprite group so that they will (theoretically) no longer be drawn

        #TODO: blit over the previous room's doors with a sprite that is larger than (64x64) so that the player can no longer collide with doors that are no longer active
       
        for door in self.activeRoom.doors:
            self.active_doors.add(door) #add the next room's doors to the active_doors sprite group to be drawn
        
          
       

g = Game() #initialize new game object
while True:
    g.clock.tick(16)
    g.new()
    g.run() #call run method
    

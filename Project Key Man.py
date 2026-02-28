import pygame
from pygame.locals import *
import numpy as np

TileMapFile = 'tmw_desert_spacing1.png'

class MainGame:
    W = 1056              # Window Width
    H = 672              # Window Height
    Window_Size = W, H

    def __init__(self):                                                 # Initializer
        pygame.init()                                                   # Initialize Game

        self.screen = pygame.display.set_mode(MainGame.Window_Size)     # First and Main Screen
        pygame.display.set_caption("Key Man")                           # Title of the Game

        self.items_on_ground = [ AnimatedItem("Wooden Sword", "woodensword_spritesheet.png", 96, 96, 5, 300, 300)]    
        # Initilatises the items that start off on the ground with name, spritesheet, tile size, amnt of frames and starting spawn position

        self.player = Player('Rusted Copper Key.png', 100, 100)         # Calls player image

        my_tileset = Tileset(TileMapFile)                               
        self.mapmaker = Map_Maker(my_tileset)                           # Initialize the tileset and map maker
        
        
        self.clock = pygame.time.Clock() 
        self.running = True                                             # State
        self.mapmaker.set_random()                                      # Generate a map immediately so the background isn't black

    def run(self):
        while self.running:
            for event in pygame.event.get():      # Checks every event happening
                if event.type == QUIT:            # Exit to Quit
                    self.running = False          # Changes state to quit

                elif event.type == KEYDOWN:             # Checks for any key pressed
                    if event.key == K_r:                               # Checks if the key is R
                        self.mapmaker.set_random()                       # Runs the randomized
                        self.screen.blit(self.mapmaker.image, (0, 0))    # Paints the created tilemap onto the self.screen 
                        pygame.display.update()                          # Refreshes the monitor

                    elif event.key == K_0:                               # Checks if the key is 0
                        self.mapmaker.set_zero()                         # Runs the set zero
                        self.screen.blit(self.mapmaker.image, (0, 0))    # Paints the created tilemap onto the self.screen 
                        pygame.display.update()                          # Refreshes the monitor


            keys = pygame.key.get_pressed()
            self.player.move(keys)

            # 2. Draw the background map first (Painter's Algorithm)
            self.screen.blit(self.mapmaker.image, (0, 0))

            for item in self.items_on_ground[:]:       # With the [:] making a copy of the list so that items can be removed
                item.draw(self.screen)

                if self.player.rect.colliderect(item.rect):       # Checks if the hitboxes collided
                    print("You picked up: ", item.name)           # Prints pickups for debugging

                    self.player.inventory.append(item.name)       
                    self.items_on_ground.remove(item)             # Adds the item to the player's inventory and removes it from the floor
                

            # 3. Draw the transparent player on top
            self.player.draw(self.screen)
            
            # 4. Refresh the monitor and tick the clock
            pygame.display.update()
            self.clock.tick(60) # Runs the game at 60 FPS

        pygame.quit()                             # Quits when self.running is false


class Tileset:                                                         # Splits up a tile map into tiles
    def __init__(self, file, size=(96, 96), margin=3, spacing=3):      # Intializes some variables notably size of the tiles, margin of the tilemap, spacing between the tiles
        self.file = file
        self.size = size
        self.margin = margin
        self.spacing = spacing
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.tiles = []                                                # Prepares a list to stores the individual tiles after cutting them up
        self.load()                                                    # Runs the load method


    def load(self):

        self.tiles = []                          # Empties the tile list
        x0 = y0 = self.margin                    # Makes sure to start cutting after the margin is taken into account
        w, h = self.rect.size                    # Saves the width and height of the tile map
        dx = self.size[0] + self.spacing         # Saves the width of an individual tile
        dy = self.size[1] + self.spacing         # Saves the height of an individual tile
        
        for x in range(x0, w, dx):
            for y in range(y0, h, dy):                               # Two for loops to go across each tile
                tile = pygame.Surface(self.size)                     # Creates a tile size surface for the tile
                tile.blit(self.image, (0, 0), (x, y, *self.size))    # Cuts out the tile from the tile map and pastes it at 0 0 of the recently created surface
                self.tiles.append(tile)                              # Adds the tile to the list of tiles

    def __str__(self):
        return f'{self.__class__.__name__} file:{self.file} tile:{self.size}'    # Handles the output of printing a tile to the terminal
    


class Map_Maker:                                                   # Creates the map
    def __init__(self, tileset, size=(7, 11), rect=None):         # Accepts the tileset, a tile x * y size and an optional rect variable
        self.size = size
        self.tileset = tileset
        self.map = np.full(size, 33, dtype=int)                 # Creates an array of zeroes representing no tiles in the map

        h, w = self.size                                     # Splits the height and width out of the size variable
        self.image = pygame.Surface((96*w, 96*h))            # Creates a surface of the tile size times the map size

        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()             # Defauls to 0 0 if no coordinates are given

    def render(self):
        m, n = self.map.shape                                 # Gets the Height and width from the zeros array
        for i in range(m):
            for j in range(n):                                # Loops through each entry
                tile = self.tileset.tiles[self.map[i, j]]     # Accesses each tile from the tile list created in the class tile set
                self.image.blit(tile, (j*96, i*96))           # Draws the tile onto the canvas

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)         # Resets the map to all 0s
        print(self.map)
        print(self.map.shape)                             # Prints for debugging purposes
        self.render()                                     # Runs the render

    def set_random(self):

        h, w = self.map.shape                              # Gets the Height and width from the zeros array

        n = len(self.tileset.tiles)                        # Saves the length of the tile list
        #self.map = np.random.randint(n, size=self.size)   # Fills the map array with random numbers between 0 and n

        for x in range(0, w):
            self.map[0, x] = 6
            self.map[h-1, x] = 8


        for y in range(0, h):
            self.map[y, 0] = 1
            self.map[y, w-1] = 13
        
        self.map[0, 0] = 0
        self.map[0, w-1] = 12
        self.map[h-1, 0] = 2
        self.map[h-1, w-1] = 14                           # Sets the border tiles accordingly edges then corners
        
            
        print(self.map)                                   # Prints for debugging purposes
        self.render()                                     # runs the render

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'   # Handles the output of printing a tilemap to the terminal  
    
class Player:                                                             # Initializes the main charachter
    def __init__(self, image_file, x, y):
        
        self.image = pygame.image.load(image_file).convert_alpha()        # convert_alpha() is essential for transparent tiles

        self.rect = self.image.get_rect()                                 # Creates a rectangle the size of the character for hitbox
        self.rect.topleft = (x, y)                                        # Sets the top left corner

        self.speed = 5                                                    # Speed
        self.inventory = []                                               # A list to store items 

    def move(self, keys):
        # pygame.key.get_pressed() allows for smooth, continuous movement
        if keys[K_w]:
            self.rect.y -= self.speed
        if keys[K_s]:
            self.rect.y += self.speed
        if keys[K_a]:
            self.rect.x -= self.speed
        if keys[K_d]:
            self.rect.x += self.speed                                          # WASD

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class AnimatedItem:
    def __init__(self, name, spritesheet_file, frame_width, frame_height, num_frames, x, y):
        self.name = name
        
        sheet = pygame.image.load(spritesheet_file).convert_alpha()        # Loads the master sprite sheet
        

        self.frames = []
        for i in range(num_frames):
            cutout_box = pygame.Rect(i * frame_width, 0, frame_width, frame_height)  # Cut out the individual frames
            

            frame_image = sheet.subsurface(cutout_box)               # Targets only the pixels inside that box
            self.frames.append(frame_image)                          # Adds the frame to the list of frames 
            

        self.current_frame = 0                                 # Starts at the first frame
        self.image = self.frames[self.current_frame]           # sets the image to the current frame
        self.rect = self.image.get_rect()                      # makes the hitbox a rectangle around the image
        self.rect.topleft = (x, y)                             # sets the top left corner of the hitbox to the top left corner of the item
        

        self.animation_timer = 0         # Animation speed controls
        self.animation_speed = 15

    def animate(self):
        self.animation_timer += 1           # Increases the timer
        if self.animation_timer >= self.animation_speed:        # Resets timer and changes frame every 15 runs
            self.animation_timer = 0      
            self.current_frame += 1  
            
            if self.current_frame >= len(self.frames):
                self.current_frame = 0                        # Loops the frame after frames are done
                
            self.image = self.frames[self.current_frame]      # sets image to the latest frame

    def draw(self, surface):
        self.animate() 
        surface.blit(self.image, self.rect.topleft)           # Draws the animations onto the screen

if __name__ == "__main__":
    game = MainGame()                                 # Sets the initializer to game
    game.run()                                        # Runs the game
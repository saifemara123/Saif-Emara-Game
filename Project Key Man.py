import pygame
from pygame.locals import *
import numpy as np

TileMap = 'tmw_desert_spacing.png'

class MainGame:
    W = 900              # Window Width
    H = 700              # Window Height
    Window_Size = W, H

    def __init__(self):                                                 # Initializer
        pygame.init()                                                   # Initialize Game
        self.screen = pygame.display.set_mode(MainGame.Window_Size)     # First and Main Screen
        pygame.display.set_caption("Key Man")                           # Title of the Game
        self.running = True                                             # State

    def run(self):
        while self.running:
            for event in pygame.event.get():      # Checks every event happening
                if event.type == QUIT:            # Exit to Quit
                    self.running = False          # Changes state to quit

                elif event.type == KEYDOWN:       # Checks for any key pressed
                    if event.key == K_l:          # Checks if the key is L   (Key_L)
                        self.load_image(TileMap)  # Runs load image on the tile map
                    elif event.key == K_r:
                        Tilemap.set_random()

        pygame.quit()                             # Quits when self.running is false

    def load_image(self, TileMap):
        self.file = TileMap                       # The tilemap is set to file
        self.image = pygame.image.load(TileMap)   # and loaded
        self.rect = self.image.get_rect()         # gets the size of the image as a rectangle saving it to self.rect


        self.screen.blit(self.image, (0, 0))      # Draws the image onto the screen with the second variable determining the coords of the top left corner
        pygame.display.update()                   # Updates the changes made to the display

game = MainGame()                                 # Sets the initializer to game
game.run()                                        # Runs run



class Tileset:                                                         # Splits up a tile map into tiles
    def __init__(self, file, size=(32, 32), margin=1, spacing=1):      # Intializes some variables notably size of the tiles, margin of the tilemap, spacing between the tiles
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
    


class Tilemap:                                                   # Creates the map
    def __init__(self, tileset, size=(10, 20), rect=None):       # Accepts the tileset, a tile x * y size and an optional rect variable
        self.size = size
        self.tileset = tileset
        self.map = np.zeros(size, dtype=int)                 # Creates an array of zeroes representing no tiles in the map

        h, w = self.size                                     # Splits the height and width out of the size variable
        self.image = pygame.Surface((32*w, 32*h))            # Creates a surface of the tile size times the map size

        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()             # Defauls to 0 0 if no coordinates are given

    def render(self):
        m, n = self.map.shape                                 # Gets the Height and width from the zeros array
        for i in range(m):
            for j in range(n):                                # Loops through each entry
                tile = self.tileset.tiles[self.map[i, j]]     # Accesses each tile from the tile list created in the class tile set
                self.image.blit(tile, (j*32, i*32))           # Draws the tile onto the canvas

    def set_zero(self):
        self.map = np.zeros(self.size, dtype=int)         # Resets the map to all 0s
        print(self.map)
        print(self.map.shape)                             # Prints for debugging purposes
        self.render()                                     # Runs the render

    def set_random(self):
        n = len(self.tileset.tiles)                       # Saves the length of the tile list
        self.map = np.random.randint(n, size=self.size)   # Fills the map array with random numbers between 0 and n
        print(self.map)                                   # Prints for debugging purposes
        self.render()                                     # runs the render

    def __str__(self):
        return f'{self.__class__.__name__} {self.size}'   # Handles the output of printing a tilemap to the terminal  
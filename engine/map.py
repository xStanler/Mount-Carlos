import pygame
import numpy as np

class Map:
    def __init__(self, tiles = [], tile_size=(16, 16), size=(42, 42), rect=None):
        self.size = size
        self.tiles = tiles
        self.tile_size = tile_size
        self.map = np.zeros(size, dtype=int)

        height, width = self.size
        x, y = self.tile_size
        self.image = pygame.Surface((width*x, height*y))

        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        h, w = self.map.shape

        # for i in range(h):
            # tile = tiles[0] #TODO: make tiles[]


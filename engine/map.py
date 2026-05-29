import pygame
import numpy as np
from pathlib import Path

class Tiles:
    def __init__(self, size=(16, 16)):
        self.tiles = dict()
        self.size = size

        assetsDir = Path(__file__).resolve().parent.parent / "assets/Tiles"

        for file in assetsDir.iterdir():
            print(file)

    def get_size(self):
        return self.size

class Map:
    def __init__(self, tiles = Tiles(), size=(42, 42), rect=None):
        self.size = size
        self.tiles = tiles
        self.map = np.zeros(size, dtype=int)

        height, width = self.size
        x, y = self.tiles.get_size()
        self.image = pygame.Surface((width*x, height*y))

        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def render(self):
        h, w = self.map.shape

        # for i in range(h):
            # tile = tiles[0] #TODO: make tiles[]

if __name__ == "__main__":
    tiles = Tiles()
    print(tiles.get_size())

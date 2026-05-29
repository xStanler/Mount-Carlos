import pygame
import numpy as np
from pathlib import Path

class Tiles:
    def __init__(self, texture_size=(16, 16), render_size=(64, 64)):
        self.tiles = dict()
        self.texture_size = texture_size
        self.render_size = render_size

        self.assetsDir = Path(__file__).resolve().parent.parent / "assets/Tiles"
        self.load()

    def load(self):
        for file in self.assetsDir.iterdir():
            if file.suffix == '.png' and not "tile" in file.stem:
                name = file.stem
                img = pygame.image.load(file).convert_alpha()
                tile = pygame.transform.scale(img, self.render_size)
                self.tiles[name] = tile

                # tile = pygame.Surface(self.texture_size)
                # tile.blit(img, (0, 0), (0, 0, *self.render_size))
                # tile = pygame.transform.scale(tile, self.render_size)
                #
                # self.tiles[name] = tile

    def get_size(self):
        return self.render_size

    def get_tiles(self):
        return self.tiles

class Map:
    def __init__(self, tiles, size=(42, 42), rect=None):
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

        for y in range(h):
            for x in range(w):
                tile = self.tiles.get_tiles()["grass"]
                if (x == 0 and (y == 0 or y == h-1)) or (x == w-1 and (y == 0 or y == h-1)):
                    tile = self.tiles.get_tiles()["wallCorner"]
                elif x == 0:
                    tile = self.tiles.get_tiles()["wallLeft"]
                elif x == w-1:
                    tile = self.tiles.get_tiles()["wallRight"]
                elif y == h-1:
                    tile = self.tiles.get_tiles()["wallBottom"]
                elif y == 0:
                    tile = self.tiles.get_tiles()["wallTop"]
                elif y == 1:
                    tile = self.tiles.get_tiles()["wall"]

                i, j = self.tiles.get_size()
                self.image.blit(tile, (x*i, y*j))

                if (x > 1 and y > 2) and x%5 == 0 and y%5==0:
                    tile = self.tiles.get_tiles()["bush"]
                    self.image.blit(tile, (x*i, y*j))

if __name__ == "__main__":
    tiles = Tiles()
    print(tiles.get_tiles())

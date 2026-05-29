import pygame
import numpy as np
from pathlib import Path
from enum import Enum

class TileType(Enum):
    GRASS = 0
    BUSH = 1
    CORNER = 2
    WALL = 3
    WALLLEFT = 4
    WALLRIGHT = 5
    WALLTOP = 6
    WALLBOTTOM = 7
    FLOWERS = 8 
    TREE = 9

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
    def __init__(self, tiles, size=(42, 43), rect=None):
        self.size = size
        self.tiles = tiles
        self.map = np.zeros(size, dtype=object)

        self.make()
        self.randomize()

        width, height = self.size
        x, y = self.tiles.get_size()
        self.image = pygame.Surface((width*x, height*y))

        if rect:
            self.rect = pygame.Rect(rect)
        else:
            self.rect = self.image.get_rect()

    def make(self):
        width, height = self.size

        for y in range(height):
            for x in range(width):
                self.map[x, y] = TileType.GRASS
                if (x == 0 and (y == 0 or y == height-1)) or (x == width-1 and (y == 0 or y == height-1)):
                    self.map[x, y] = TileType.CORNER
                elif x == 0:
                    self.map[x, y] = TileType.WALLLEFT
                elif x == width-1:
                    self.map[x, y] = TileType.WALLRIGHT
                elif y == height-1:
                    self.map[x, y] = TileType.WALLBOTTOM
                elif y == 0:
                    self.map[x, y] = TileType.WALLTOP
                elif y == 1:
                    self.map[x, y] = TileType.WALL

    def randomize(self):
        x, y = np.random.randint(360, size=2)
        
        noisePath = Path(__file__).resolve().parent.parent / "assets/Maps"
        noiseMap = pygame.image.load(noisePath / "noiseMap2.png").convert_alpha()

        rect = pygame.Rect(x, y, 40, 40)
        subsurface = noiseMap.subsurface(rect)

        w, h = subsurface.get_size()

        for yMap in range(h):
            for xMap in range(w):
                color = subsurface.get_at((xMap, yMap))
                rng = np.random.randint(100)

                if color == (0, 0, 0, 255):
                    self.map[xMap+1, yMap+2] = TileType.BUSH
                elif color == (255, 255, 255, 255):
                    self.map[xMap+1, yMap+2] = TileType.GRASS
                    if rng <= 15:
                        self.map[xMap+1, yMap+2] = TileType.FLOWERS

                if rng <= 5:
                    self.map[xMap+1, yMap+2] = TileType.TREE


    def render(self):
        w, h = self.map.shape

        for y in range(h):
            for x in range(w):
                tileType = self.map[x, y]
                tile = self.tiles.get_tiles()["bush"]

                match tileType:
                    case TileType.GRASS | TileType.BUSH | TileType.TREE:
                        tile = self.tiles.get_tiles()["grass"]
                    case TileType.FLOWERS:
                        tile = self.tiles.get_tiles()["flowers"]
                    case TileType.CORNER:
                        tile = self.tiles.get_tiles()["wallCorner"]
                    case TileType.WALLLEFT:
                        tile = self.tiles.get_tiles()["wallLeft"]
                    case TileType.WALLRIGHT:
                        tile = self.tiles.get_tiles()["wallRight"]
                    case TileType.WALLBOTTOM:
                        tile = self.tiles.get_tiles()["wallBottom"]
                    case TileType.WALLTOP:
                        tile = self.tiles.get_tiles()["wallTop"]
                    case TileType.WALL:
                        tile = self.tiles.get_tiles()["wall"]

                i, j = self.tiles.get_size()
                self.image.blit(tile, (x*i, y*j))

                if tileType == tileType.BUSH:
                    tile = self.tiles.get_tiles()["bush"]
                    self.image.blit(tile, (x*i, y*j))
                elif tileType == tileType.TREE:
                    tile = self.tiles.get_tiles()["tree"]
                    self.image.blit(tile, (x*i, y*j))

if __name__ == "__main__":
    tiles = Tiles()
    print(tiles.get_tiles())

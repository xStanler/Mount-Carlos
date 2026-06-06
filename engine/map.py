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
        self.solid_tiles = {
                TileType.TREE,
                TileType.CORNER,
                TileType.WALL,
                TileType.WALLLEFT,
                TileType.WALLRIGHT,
                TileType.WALLTOP,
                TileType.WALLBOTTOM
                }
        self.trigger_tiles = {
                TileType.BUSH,
                }
        
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

    def is_solid_at_pixel(self, pixel_x, pixel_y):
        tile_w, tile_h = self.tiles.get_size()
        map_x = int(pixel_x // tile_w)
        map_y = int(pixel_y // tile_h)

        if map_x < 0 or map_x >= self.size[0] or map_y < 0 or map_y >= self.size[1]:
            return True

        return self.map[map_x, map_y] in self.tiles.solid_tiles

    def check_trigger_at_pixel(self, pixel_x, pixel_y):
        tile_w, tile_h = self.tiles.get_size()
        map_x = int(pixel_x // tile_w)
        map_y = int(pixel_y // tile_h)

        if map_x < 0 or map_x >= self.size[0] or map_y < 0 or map_y >= self.size[1]:
            return None

        tile_type = self.map[map_x, map_y]

        if tile_type in self.tiles.trigger_tiles:
            return tile_type

        return None
    
    def player_starting_pos(self):
        for dy in range(17, 27):
            for dx in range(16, 26):
                if (self.map[dx, dy] == TileType.GRASS or self.map[dx, dy] == TileType.BUSH) and (self.map[dx, dy-1] == TileType.GRASS or self.map[dx, dy-1] == TileType.BUSH) and (self.map[dx + 1, dy] == TileType.GRASS or self.map[dx + 1, dy] == TileType.BUSH):
                    return dx, dy

        return 0, 0

    def render(self, screen, camera):
        w, h = self.map.shape

        for y in range(h):
            for x in range(w):
                tileType = self.map[x, y]
                tile = self.tiles.get_tiles()["bush"]

                i, j = self.tiles.get_size()
                screen_x = int(x*i - camera.x)
                screen_y = int(y*j - camera.y)

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

                # screen.blit(tile, (x*i, y*j))
                screen.blit(tile, (screen_x, screen_y))
                # self.image.blit(tile, (x*i, y*j))

                if tileType == tileType.BUSH:
                    tile = self.tiles.get_tiles()["bush"]
                    # screen.blit(tile, (x*i, y*j))
                    screen.blit(tile, (screen_x, screen_y))
                    # self.image.blit(tile, (x*i, y*j))
                elif tileType == tileType.TREE:
                    tile = self.tiles.get_tiles()["tree"]
                    # screen.blit(tile, (x*i, y*j))
                    screen.blit(tile, (screen_x, screen_y))
                    # self.image.blit(tile, (x*i, y*j))

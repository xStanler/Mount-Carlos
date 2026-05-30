from engine.map import Map, Tiles
from engine.player import Player
from engine.camera import Camera
import pygame
from pygame.locals import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Mount Carlos")

        self.screen = pygame.display.set_mode((640, 640), pygame.RESIZABLE | pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        
        self.running = True

        self.camera = Camera()

        self.tiles = Tiles()
        self.map = Map(self.tiles)

        self.player = Player()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                event.size,
                pygame.RESIZABLE | pygame.SCALED
            )

    def update(self):
        self.player.update(self.map)
        self.camera.update(self.player, self.screen)

    def render(self):
        self.screen.fill((192, 203, 220))
        self.map.render(self.screen, self.camera)
        self.player.render(self.screen, self.camera)
        pygame.display.flip()

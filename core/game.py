from engine.map import Map, Tiles
import pygame
from pygame.locals import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Mount Carlos")

        self.screen = pygame.display.set_mode((640, 640), pygame.RESIZABLE | pygame.SCALED)
        self.clock = pygame.time.Clock()
        
        self.running = True

        self.tiles = Tiles()
        self.map = Map(self.tiles)
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

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
        pass

    def render(self):
        self.screen.fill((133, 198, 105))
        self.map.render()
        self.screen.blit(self.map.image, self.map.rect)
        pygame.display.flip()

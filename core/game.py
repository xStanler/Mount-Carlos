from engine.map import Map, Tiles
from engine.player import Player
from engine.camera import Camera
from ui.menus import MainMenu
import pygame
from pygame.locals import *
from enum import Enum

class GameState(Enum):
    MENU = 0,
    LOADING = 1,
    GAME = 2,
    PAUSE = 3

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Mount Carlos")

        self.screen = pygame.display.set_mode((640, 640), pygame.RESIZABLE | pygame.SCALED, vsync=1)
        self.clock = pygame.time.Clock()
        
        self.running = True
        self.main_menu = MainMenu(*self.screen.get_size())
        self.game_state = GameState.MENU

        self.camera = Camera()

        self.tiles = Tiles()
        self.map = Map(self.tiles)

        self.player = Player()
    
    def run(self):
        self.mouse_clicked = False

        while self.running:
            self.mouse_pos = pygame.mouse.get_pos()
            self.handle_events()
            self.handle_states()
            # self.update()
            # self.render()

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

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.mouse_clicked = True

    def handle_states(self):
        if self.game_state == GameState.MENU:
            menu_action = self.main_menu.update(self.mouse_pos, self.mouse_clicked)

            if menu_action == "START":
                self.game_state = GameState.GAME
            elif menu_action == "QUIT":
                self.running = False

            self.main_menu.render(self.screen)
            pygame.display.flip()
        elif self.game_state == GameState.GAME:
            self.update()
            self.render()


    def update(self):
        self.player.update(self.map)
        self.camera.update(self.player, self.screen)

    def render(self):
        self.screen.fill((192, 203, 220))
        self.map.render(self.screen, self.camera)
        self.player.render(self.screen, self.camera)
        pygame.display.flip()

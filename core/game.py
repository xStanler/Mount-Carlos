from engine.map import Map, Tiles
from engine.player import Player
from engine.camera import Camera
from ui.menus import MainMenu, PauseMenu
import pygame
from pygame.locals import *
from pathlib import Path
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

        icon_path = Path(__file__).parent.parent / "assets/icon.png"
        self.icon = pygame.image.load(icon_path).convert_alpha()
        pygame.display.set_icon(self.icon)
        
        self.running = True
        self.main_menu = MainMenu(*self.screen.get_size())
        self.pause_menu = PauseMenu(*self.screen.get_size())
        self.game_state = GameState.MENU

        self.camera = Camera()

        self.tiles = Tiles()
        self.map = Map(self.tiles)

        sx, sy = self.map.player_starting_pos()
        print(sx, sy)
        self.player = Player(sx, sy)
    
    def run(self):
        while self.running:
            self.mouse_clicked = False
            self.mouse_pos = pygame.mouse.get_pos()
            self.handle_events()
            self.handle_states()
            # self.update()
            # self.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen = pygame.display.set_mode(
                event.size,
                pygame.RESIZABLE | pygame.SCALED,
                vsync=1
            )

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.mouse_clicked = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.game_state = GameState.PAUSE

    def handle_states(self):
        if self.game_state == GameState.MENU:
            menu_action = self.main_menu.update(self.mouse_pos, self.mouse_clicked)

            if menu_action == "START":
                self.game_state = GameState.GAME
            elif menu_action == "QUIT":
                self.running = False

            self.main_menu.render(self.screen)
        elif self.game_state == GameState.PAUSE:
            pause_action = self.pause_menu.update(self.mouse_pos, self.mouse_clicked)

            if pause_action == "CONTINUE":
                self.game_state = GameState.GAME
            elif pause_action == "QUIT":
                self.running = False

            self.pause_menu.render(self.screen)
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
        # pygame.display.flip()

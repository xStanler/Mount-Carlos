from engine.player import Player
from engine.camera import Camera
import pygame
from pathlib import Path

class BattleUI:
    def __init__(self, screen, player, enemy = None):
        self.screen = screen
        self.player = player
        self.enemy = enemy
        self.screen_width, self.screen_height = screen.get_size()

        groundPath = Path(__file__).parent.parent / "assets/battle_grass.png"
        self.ground = pygame.image.load(groundPath).convert_alpha()
        self.ground = pygame.transform.scale_by(self.ground, 2)
    
    def show_player(self, screen):
        self.player.moving = False
        self.player.direction = "right"
        sprite = self.player.current_sprite()

        screen.blit(sprite, (self.ground.get_size()[0]//3, screen.get_size()[1] - self.ground.get_size()[1]*3))

        self.player.animation_timer += 1

        if self.player.animation_timer >= 10:
            self.player.animation_timer = 0
            self.player.animation_frame = (self.player.animation_frame + 1) % 6

    def show_enemy(self, screen):
        pass

    def show_moves(self, screen):
        moves = self.player.moves

        moves_ui = pygame.Rect(int(self.ground.get_size()[0]), int(screen.get_size()[1] - self.ground.get_size()[1]*2), screen.get_size()[0]//2, self.ground.get_size()[1]*2)
        pygame.draw.rect(screen, (255, 255, 255), moves_ui)

    def render(self, screen):
        screen.fill((183, 221, 166))
        screen.blit(self.ground, (screen.get_size()[0] - self.ground.get_size()[0] - 50, 100))
        screen.blit(self.ground, (50, screen.get_size()[1] - self.ground.get_size()[1] - 100))

        self.show_player(screen)
        self.show_moves(screen)
        self.show_enemy(screen)


#WARNING: DELETE AFTER DEBUGGING
def handle_events():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

    return True

if __name__ == "__main__":
    pygame.init()
    
    screen = pygame.display.set_mode((640, 640), pygame.SCALED, vsync=1)
    clock = pygame.time.Clock()

    camera = Camera()
    player = Player(0, 0)

    battle = BattleUI(screen, player)

    running = True

    while running:
        running = handle_events()

        battle.render(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

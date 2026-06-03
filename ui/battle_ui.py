from engine.player import Player
from engine.enemy import Enemy, EnemyType
from engine.camera import Camera
import pygame
from pathlib import Path

class BattleUI:
    def __init__(self, screen, player, enemy):
        self.screen = screen
        self.player = player
        self.enemy = enemy
        self.screen_width, self.screen_height = screen.get_size()

        fontPath = Path(__file__).parent.parent / "assets/VT323-Regular.ttf"
        self.move_font = pygame.font.Font(str(fontPath), 32)
        groundPath = Path(__file__).parent.parent / "assets/battle_grass.png"
        self.ground = pygame.image.load(groundPath).convert_alpha()
        self.ground = pygame.transform.scale_by(self.ground, 2)
    
    def show_player(self, screen):
        self.player.moving = False
        self.player.direction = "right"
        sprite = self.player.current_sprite()

        screen.blit(sprite, (self.ground.get_size()[0]//2 - self.player.scale // 1.5, int(screen.get_size()[1] - self.ground.get_size()[1]*2) - self.player.scale*2.5))

        self.player.animation_timer += 1

        if self.player.animation_timer >= 10:
            self.player.animation_timer = 0
            self.player.animation_frame = (self.player.animation_frame + 1) % 6

    def show_enemy(self, screen):

        screen.blit(self.enemy.sprites.idle[self.enemy.animation_frame], (screen.get_size()[0] - self.ground.get_size()[0] + self.enemy.sprites.idle_size[0], 100 - self.enemy.sprites.idle_size[1]))

        self.enemy.animation_timer += 1

        if self.enemy.animation_timer >= 20:
            self.enemy.animation_timer = 0
            self.enemy.animation_frame = (self.enemy.animation_frame + 1) % self.enemy.sprites.idle_len

    def show_moves(self, screen):
        moves = self.player.moves

        moves_ui = pygame.Rect(0, int(screen.get_size()[1] - self.ground.get_size()[1]*2), screen.get_size()[0], self.ground.get_size()[1]*2)
        pygame.draw.rect(screen, (255, 255, 255), moves_ui)
        pygame.draw.rect(screen, (0, 0, 0), moves_ui, 4)
        
        moves_name = [move.name for move in moves]
        moves_name.append("Forfeit")
        for i, name in enumerate(moves_name):
            move = self.move_font.render(f"{i+1}. {name}", True, (0, 0, 0))
            screen.blit(move, ( (i%2)*275 + 50, (i//2)*75 + int(screen.get_size()[1] - self.ground.get_size()[1]*1.6)))

    def render(self, screen):
        screen.fill((183, 221, 166))
        screen.blit(self.ground, (screen.get_size()[0] - self.ground.get_size()[0] - 50, 100))
        screen.blit(self.ground, (50, screen.get_size()[1] - self.ground.get_size()[1] - 160))

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
    # screen = pygame.display.set_mode((1280, 900), pygame.SCALED, vsync=1)
    clock = pygame.time.Clock()

    camera = Camera()
    player = Player(0, 0)
    enemy = Enemy("Draco", EnemyType.GRASS)

    battle = BattleUI(screen, player, enemy)

    running = True

    while running:
        running = handle_events()

        battle.render(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

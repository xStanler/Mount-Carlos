from engine.player import Player
from engine.enemy import Enemy, State
from engine.camera import Camera
import pygame
from pathlib import Path

class BattleUI:
    def __init__(self, screen, player, enemy):
        self.screen = screen
        self.player = player
        self.enemy = enemy

        fontPath = Path(__file__).parent.parent / "assets/VT323-Regular.ttf"
        self.font = pygame.font.Font(str(fontPath), 32)
        groundPath = Path(__file__).parent.parent / "assets/battle_grass.png"
        self.ground = pygame.image.load(groundPath).convert_alpha()
        self.ground = pygame.transform.scale_by(self.ground, 2)
    
    def show_player(self):
        sprite = self.player.battle_sprite()

        self.screen.blit(sprite, (self.ground.get_size()[0]//2 - self.player.scale // 1.5, int(self.screen.get_size()[1] - self.ground.get_size()[1]*2) - self.player.scale*2.5))

        self.player.update_animation()
        
    def show_enemy(self):
        size = (0, 0)
        currentSprites = self.enemy.get_sprites()
        match self.enemy.state:
            case State.IDLE:
                size = self.enemy.sprites.idle_size
            case State.ATTACK:
                size = self.enemy.sprites.attack_size
            case State.HURT:
                size = self.enemy.sprites.hurt_size

        self.screen.blit(currentSprites[self.enemy.animation_frame], (self.screen.get_size()[0] - self.ground.get_size()[0] + size[0], 100 - size[1]))

        # self.enemy.update_animation()

    def show_moves(self):
        moves = self.player.moves

        moves_ui = pygame.Rect(0, int(self.screen.get_size()[1] - self.ground.get_size()[1]*2), self.screen.get_size()[0], self.ground.get_size()[1]*2)
        pygame.draw.rect(self.screen, (255, 255, 255), moves_ui)
        pygame.draw.rect(self.screen, (0, 0, 0), moves_ui, 4)
        
        moves_name = [move.name for move in moves]
        for i, name in enumerate(moves_name):
            move = self.font.render(f"{i+1}. {name} ({moves[i].uses})", True, (0, 0, 0))
            self.screen.blit(move, ( (i%2)*275 + 50, (i//2)*75 + int(self.screen.get_size()[1] - self.ground.get_size()[1]*1.6)))

    def show_health(self, entity, x, y):
        health_ui = pygame.Rect(x, y, 300, 100)
        health_text = self.font.render(f"{entity.name}: {entity.health} HP", True, (0, 0, 0))

        pygame.draw.rect(self.screen, (255, 255, 255), health_ui)
        pygame.draw.rect(self.screen, (0, 0, 0), health_ui, 4)

        self.screen.blit(health_text, (x + 20, y + 20))
        pygame.draw.rect(self.screen, (120, 120, 120), pygame.Rect(x + 20, y + 60, 260, 10))
        pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(x + 20, y + 60, 260 * (entity.health / entity.HEALTH), 10))

    # def show_mesages(self):
    #     y = 20
    #     for message in list(self.battle.message_queue):
    #         text = self.font.render(message, True, (0, 0, 0))
    #         self.screen.blit(text, (20, y))
    #         y += 30

    def render(self):
        self.screen.fill((183, 221, 166))
        self.screen.blit(self.ground, (self.screen.get_size()[0] - self.ground.get_size()[0] - 50, 100))
        self.screen.blit(self.ground, (50, self.screen.get_size()[1] - self.ground.get_size()[1] - 160))

        self.show_player()
        self.show_moves()
        #NOTE: TEST ANIMATIONS
        # if self.enemy.animation_frame == 0:
        #     self.enemy.state = (self.enemy.state+1)%3
        #     self.enemy.animation_frame = 1
        self.show_enemy()
        self.show_health(self.player, self.screen.get_size()[0] - 300, self.screen.get_size()[1] - self.ground.get_size()[1] - 170)
        self.show_health(self.enemy, 0, 20)


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
    player = Player()
    enemy = Enemy()

    battle = BattleUI(screen, player, enemy)

    running = True

    while running:
        running = handle_events()

        battle.render()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

from engine.player import Player
from engine.enemy import Enemy, State
from engine.camera import Camera
from engine.battle import BattleState
import pygame
from pathlib import Path

class BattleUI:
    def __init__(self, screen, player, enemy, battle):
        self.screen = screen
        self.player = player
        self.enemy = enemy
        self.battle = battle

        fontPath = Path(__file__).parent.parent / "assets/VT323-Regular.ttf"
        self.font = pygame.font.Font(str(fontPath), 32)
        self.fontMessage = pygame.font.Font(str(fontPath), 14)
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

    def show_messages(self):
        if self.battle.message == None:
            return

        message = self.battle.message

        rect = pygame.Rect(
                self.screen.get_width() // 2 - 250,
                self.screen.get_height() // 2 - 50,
                500,
                100
                )
        pygame.draw.rect(self.screen, (255, 255, 255), rect)
        pygame.draw.rect(self.screen, (0, 0, 0), rect, 4)

        text = self.fontMessage.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(center=rect.center)
        self.screen.blit(text, text_rect)

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
        if self.battle.state == BattleState.PLAYER_MESSAGE or self.battle.state == BattleState.ENEMY_MESSAGE:
            self.show_messages()

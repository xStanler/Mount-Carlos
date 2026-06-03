from engine.player import Player
from engine.enemy import Enemy, State
from collections import deque
import pygame

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

        self.message_queue = deque(maxlen=5)
        self.turn = "player"

        self.finished = False
        self.result = None

    def player_move(self, move_idx):
        move = self.player.moves[move_idx]

        if move.uses <= 0:
            self.message_queue.append(f"Nie można użyć {move.name}!")
            return
        move.uses -= 1

        self.enemy.health -= move.attack
        self.player.health += move.heal

        self.enemy.health = max(0, self.enemy.health)
        self.player.health = min(self.player.health, self.player.HEALTH)

        self.message_queue.append(self.create_message(self.player.name, move))

        self.enemy.state = State.HURT

        self.turn = "enemy"

    def enemy_move(self, move_idx):
        self.message_queue.append(f"{self.enemy.name} zrobił nic!")
        self.enemy.state = State.IDLE
        
        self.turn = "player"

    def create_message(self, attacker, move):
        parts = [f"{attacker} użył {move.name}"]

        if move.attack > 0:
            parts.append(f"zadając {move.attack} obrażeń")

        if move.heal > 0:
            parts.append(f"lecząc {move.heal} HP")
        else:
            parts.append(f"tracąc {-move.heal} HP")

        return ", ".join(parts) + "."

    def check_end(self):
        if self.player.health <= 0:
            self.finished = True
            self.result = "lose"

        if self.enemy.health <= 0:
            self.finished = True
            self.result = "win"

    def handle_event(self, event):
        if self.turn != "player":
            self.enemy_move(0)
        
        # if event.type != pygame.KEYDOWN:
        #     return

        if event.key == pygame.K_1:
            self.player_move(0)
        elif event.key == pygame.K_2:
            self.player_move(1)
        elif event.key == pygame.K_3:
            self.player_move(2)
        elif event.key == pygame.K_4:
            self.player_move(3)


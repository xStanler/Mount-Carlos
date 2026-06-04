from engine.player import Player
from engine.enemy import Enemy, State
from utils.move import Move
from ai.simulation import RandomChoice
from collections import deque
import pygame
from enum import Enum

class BattleState(Enum):
    PLAYER_TURN = 0
    PLAYER_MESSAGE = 1
    ENEMY_TURN = 2
    ENEMY_MESSAGE = 3 
    FINISHED = 4

class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.enemyMove = self.enemy.moves[0]

        self.message_queue = None
        self.state = BattleState.PLAYER_TURN

        self.finished = False
        self.result = None

    def player_move(self, move_idx):
        move = self.player.moves[move_idx]

        if move.uses <= 0:
            self.message = f"Nie można użyć {move.name}!"
            self.state = BattleState.PLAYER_MESSAGE
            return
        move.uses -= 1

        self.enemy.health -= move.attack
        self.player.health += move.heal

        self.enemy.health = max(0, self.enemy.health)
        self.player.health = min(self.player.health, self.player.HEALTH)

        self.message = self.create_message(self.player.name, move)

        self.enemy.state = State.HURT
        self.enemy.animation_frame = 0
        self.enemy.animation_finished = False

        self.state = BattleState.PLAYER_MESSAGE

    def enemy_move(self):
        enemyAI = RandomChoice(self.enemy.moves)
        self.enemyMove = enemyAI.chooseMove()

        self.enemy.state = State.ATTACK
        self.enemy.animation_done = False
        self.enemy.animation_frame = 0

        self.message = None

    def resolve_enemy_move(self):
        move = self.enemyMove

        if move.uses < 0:
            return

        move.uses -= 1
        self.player.health -= move.attack
        self.enemy.health += move.heal

        self.player.health = max(0, self.player.health)
        self.enemy.health = min(self.enemy.health, self.enemy.HEALTH)

        self.message = self.create_message(self.enemy.name, move)
        self.state = BattleState.ENEMY_MESSAGE

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
            self.message = f"{self.player.name} pokonał {self.enemy.name}"
            self.result = "win"

    def update(self):
        if self.state == BattleState.ENEMY_TURN:
            self.enemy.update_animation()

            if self.enemy.animation_done:
                self.resolve_enemy_move()

    def handle_event(self, event):
        if self.state == BattleState.PLAYER_MESSAGE:
            if event.key == pygame.K_RETURN:
                self.message = None
                self.state = BattleState.ENEMY_TURN
                self.enemy_move()

        if self.state == BattleState.ENEMY_MESSAGE:
            if event.key == pygame.K_RETURN:
                self.message = None
                self.enemy.state = State.IDLE
                self.enemy.animation_frame = 0
                self.state = BattleState.PLAYER_TURN
                
        if self.state == BattleState.PLAYER_TURN: 
            if event.key == pygame.K_1:
                self.player_move(0)
            elif event.key == pygame.K_2:
                self.player_move(1)
            elif event.key == pygame.K_3:
                self.player_move(2)
            elif event.key == pygame.K_4:
                self.player_move(3)


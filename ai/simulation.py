import numpy as np
from dataclasses import dataclass
from copy import deepcopy
from utils.move import Move

@dataclass
class CurrentBattleState:
    player_hp: int
    enemy_hp: int

    player_moves: list
    enemy_moves: list

    player_turn: bool

def apply_move(state: CurrentBattleState, move: Move, enemy_turn: bool):
    if enemy_turn:
        state.player_hp -= move.attack
        state.enemy_hp += move.heal

        state.player_hp = max(0, state.player_hp)
        state.enemy_hp = min(state.enemy_hp, 9999)

    else:
        state.enemy_hp -= move.attack
        state.player_hp += move.heal

        state.enemy_hp = max(0, state.enemy_hp)
        state.player_hp = min(state.player_hp, 9999)

def random_move(moves):
    available = [m for m in moves if m.uses > 0]

    if not available:
        return None

    return available[np.random.randint(len(available))]

def rollout(state: CurrentBattleState):
    state = deepcopy(state)

    while True:
        if state.player_hp <= 0:
            return True
        if state.enemy_hp <= 0:
            return False

        if state.player_turn:
            move = random_move(state.player_moves)

            if move:
                move.uses -= 1
                apply_move(state, move, False)
        else:
            move = random_move(state.enemy_moves)

            if move:
                move.uses -= 1
                apply_move(state, move, True)

        state.player_turn = not state.player_turn

class RandomChoice:
    def __init__(self, moves):
        self.moves = moves

    def choose_move(self):
        # rng = np.random.randint(len(self.moves))
        #
        # return self.moves[rng]
        return random_move(self.moves)

class MonteCarloRolloutAI:
    def __init__(self, player, enemy, simulations = 500):
        self.player = player
        self.enemy = enemy
        self.simulations = simulations

    def build_state(self):
        return CurrentBattleState(
                player_hp=self.player.health,
                enemy_hp=self.enemy.health,
                player_moves=self.player.moves,
                enemy_moves=self.enemy.moves,
                player_turn=False
                )

    def evaluate_move(self, state, move_idx):
        wins = 0

        for _ in range(self.simulations):
            sim_state = deepcopy(state)

            move = sim_state.enemy_moves[move_idx]

            if move.uses <= 0:
                continue

            move.uses -= 1
            apply_move(sim_state, move, True)
            sim_state.player_turn = True

            if rollout(sim_state):
                wins += 1
        
        return wins
    
    def choose_move(self):
        state = self.build_state()

        best_move = None
        best_score = -1

        for i, move in enumerate(self.enemy.moves):
            if move.uses <= 0:
                continue

            score = self.evaluate_move(state, i)

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

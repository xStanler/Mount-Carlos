from ai.simulation import CurrentBattleState
import numpy as np
import math
import random
import copy

class Node:
    def __init__(self, state, parent=None, move=None, available_moves=None):
        self.state = state
        self.parent = parent
        self.move = move

        self.children = []

        self.visits = 0
        self.wins = 0

        self.untried_moves = []

        if available_moves:
            self.untried_moves = available_moves.copy()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

class MonteCarloAI:
    def __init__(self, state, iterations=1000, exploration=1.4):
        self.iterations = iterations
        self.exploration = exploration
        self.root_state = state

    def uct(self, node):
        if node.visits == 0:
            return float("inf")

        return node.wins / node.visits + self.exploration * math.sqrt(math.log(node.parent.visits) / node.visits)


    def select(self, node):
        while node.children and node.is_fully_expanded():
            node = max(node.children, key=self.uct)

        return node

    def simulate(self, state, move):
        state = copy.deepcopy(state)

        move = copy.deepcopy(move)
        move.uses -= 1
        
        if state.player_turn:
            state.enemy_hp -= move.attack
            state.player_hp += move.heal

            state.enemy_hp = max(0, state.enemy_hp)
            state.player_hp = min(state.player_hp, 9999)
            
        else:
            state.player_hp -= move.attack
            state.enemy_hp += move.heal

            state.player_hp = max(0, state.player_hp)
            state.enemy_hp = min(state.enemy_hp, 9999)

        return CurrentBattleState(
                player_hp = state.player_hp,
                enemy_hp = state.enemy_hp,
                player_moves = state.player_moves,
                enemy_moves = state.enemy_moves,
                player_turn = not state.player_turn
                )


    def expand(self, node, moves):
        move = random.choice(node.untried_moves)

        node.untried_moves.remove(move)

        new_state = self.simulate(node.state, move)

        if new_state.player_turn:
            available_moves = [m for m in new_state.player_moves if m.uses > 0]
        else:
            available_moves = [m for m in new_state.enemy_moves if m.uses > 0]

        child = Node(new_state, parent=node, move=move, available_moves=available_moves)

        node.children.append(child)

        return child
    
    def random_move(self, moves):
        available = [m for m in moves if m.uses > 0]
        
        if not available:
            return None

        return random.choice(available)

    def rollout(self, state):
        MAX_TURNS = 30
        state = copy.deepcopy(state)

        turns = 0
        while turns < MAX_TURNS and state.player_hp > 0 and state.enemy_hp > 0:
            if state.player_turn:
                move = self.random_move(state.player_moves)
            else:
                move = self.random_move(state.enemy_moves)

            if move is None:
                break

            state = self.simulate(state, move)
            turns += 1

        return 1 if state.player_hp <= 0 else 0

    def backprop(self, node, result):
        while node:
            node.visits += 1
            node.wins += result
            node = node.parent

    #NOTE: MCTS -> renamed to choose_move()
    def mcts(self):
        if self.root_state.player_turn:
            moves = [m for m in self.root_state.player_moves if m.uses > 0]
        else:
            moves = [m for m in self.root_state.enemy_moves if m.uses > 0]

        root  = Node(self.root_state, available_moves=moves)

        for _ in range(self.iterations):
            node = self.select(root)

            if node.state.player_turn:
                child = self.expand(node, node.state.player_moves)
            else:
                child = self.expand(node, node.state.enemy_moves)
            
            if child is None:
                child = node

            result = self.rollout(child.state)

            self.backprop(child, result)

        best = max(root.children, key=lambda n: n.visits)
        return best.move

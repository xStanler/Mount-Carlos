import math
import random
import copy

class Node:
    def __init__(self, state, parent=None, move=None):
        self.state = state
        self.parent = parent
        self.move = move

        self.children = []

        self.visits = 0
        self.wins = 0

class State:
    def __init__(self, player_hp, enemy_hp, player_turn):
        self.player_hp = player_hp
        self.enemy_hp = enemy_hp
        self.player_turn = player_turn

def uct(node):
    if node.visits == 0:
        return float("inf")

    return node.wins / node.visits + 1.4 * math.sqrt(math.log(node.parent.visits) / node.visits)

def select(node):
    while node.children:
        node = max(node.children, key=uct)

    return node

def expand(node, moves):
    for move in moves:
        new_state = simulate(node.state, move)
        child = Node(new_state, parent=node, move=move)
        node.children.append(child)

def rollout(state):
    state = copy(state)

    while state.player_hp > 0 and state.enemy_hp > 0:
        if state.player_turn:
            move = random_player_move()
        else:
            move = random_enemy_move()

        state = simulate(state, move)

        state.player_turn = not state.player_turn

    return 1 if state.enemy_hp <= 0 else 0

def backprop(node, result):
    while node:
        node.visits += 1
        node.wins += result
        node = node.parent

def mcts(root_state, enemy_moves, iterations=500):
    root  = Node(root_state)

    for _ in range(iterations):
        node = select(root)

        expand(node, enemy_moves)
        child = random.choice(node.children)

        result = rollout(child.state)

        backprop(child, result)

    best = max(root.children, key=lambda n: n.visits)
    return best.move

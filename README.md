# 🏔️ Mount Carlos

Mount Carlos is a 2D pixel-art RPG written in Python using Pygame.

The player takes control of Carlos, explores a procedurally generated world, discovers enemies hidden in bushes, and fights them in turn-based battles.

The primary objective of this project was not only to create a turn-based RPG game, but also to explore and implement Monte Carlo based decision-making algorithms in a real-time interactive environment.

---

## Features

### 🌍 Exploration

- Large tile-based map
- Procedural environment generation using noise maps
- Trees, flowers, bushes and walls
- Camera following the player
- Collision detection system

### 🧍 Player

- Animated character sprite
- Walking and idle animations
- Four unique abilities:
  - Healing Axe
  - Heal
  - Quick Attack
  - Strong Attack

### 👾 Enemies

Five enemy classes:

- Fire
- Water
- Grass
- Dragon
- Mythic

Each enemy:

- Has unique sprites
- Has unique attacks
- Receives random additional moves
- Has randomized HP

### ⚔️ Battle System

Turn-based combat system.

Players choose abilities using keys:

| Key | Action |
|-------|-------|
| 1 | Move 1 |
| 2 | Move 2 |
| 3 | Move 3 |
| 4 | Move 4 |
| Enter | Continue dialogue |

Battle features:

- Health bars
- Battle messages
- Attack animations
- Healing mechanics
- Limited move uses

### 🤖 AI

Informations in sction at the end of this document.

---

## Controls

### Exploration

| Key | Action |
|-------|-------|
| W | Move Up |
| A | Move Left |
| S | Move Down |
| D | Move Right |
| Arrow Keys | Alternative movement |

### Battles

| Key | Action |
|-------|-------|
| 1-4 | Select move |
| Enter | Continue |

---

## Project Structure

```text
MountCarlos/
│
├── ai/
│   ├── simulation.py
│   └── monte_carlo.py
│
├── assets/
│   ├── Player/
│   ├── Enemies/
│   ├── Tiles/
│   └── Maps/
│
├── core/
│   ├── game.py
│   └── settings.py
│
├── engine/
│   ├── player.py
│   ├── enemy.py
│   ├── map.py
│   ├── battle.py
│   └── camera.py
│
├── ui/
│   ├── battle_ui.py
│   ├── end.py
│   ├── menus.py
│   └── how_to_play.py
│
├── utils/
│   └── move.py
│
├── screenshots/
│
└── main.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/xStanler/Mount-Carlos
cd MountCarlos
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```cmd
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install pygame numpy
```

Run the game:

```bash
python main.py
```

---

## Technologies

- Python 3.12+
- Pygame
- NumPy

---

## Screenshots

![Main Menu](https://github.com/xStanler/Mount-Carlos/blob/master/screenshots/MainMenu.png?raw=true =200)


![Settings](https://github.com/xStanler/Mount-Carlos/blob/master/screenshots/Settings.png?raw=true =200)


![How to play](https://github.com/xStanler/Mount-Carlos/blob/master/screenshots/HowToPlay.png?raw=true =200)


![Gameplay](https://github.com/xStanler/Mount-Carlos/blob/master/screenshots/Gameplay.png?raw=true =200)


![Battle](https://github.com/xStanler/Mount-Carlos/blob/master/screenshots/Battle.png?raw=true =200)



---

## Author

Created by Stanisław Chmielewski.

# 🤖 Artificial Intelligence

Mount Carlos contains two enemy AI systems:

## Random AI (difficulty: easy)

The basic AI chooses one of the available moves randomly.

This implementation was primarily used for testing and balancing the combat system.

---

## Monte Carlo Tree Search (MCTS) (difficulty: medium)

The advanced AI uses a Monte Carlo algorithm to determine the most promising move.

Unlike a simple rule-based opponent, the enemy attempts to predict the future outcome of a battle by simulating many possible combat sequences before making a decision.

---

## Monte Carlo Tree Search (MCTS) (difficulty: hard)

The advanced AI uses a Monte Carlo Tree Search algorithm to determine the most promising move.

The key difference between this and previous algorithm is, this one remembers moves and only expands the decision tree. It not only saves time, but it allows for us to get whole battle log of moves.

### How it works

For every possible enemy move:

1. A virtual copy of the current battle state is created.
2. The move is applied to the copied state.
3. Hundreds of simulated battles (rollouts) are performed.
4. During each simulation both sides perform legal moves until the battle ends.
5. The result is recorded as either:
   - enemy victory
   - enemy defeat
6. The win rate of each move is calculated.
7. The move with the highest estimated chance of victory is selected.

### Tree Structure

Each node of the search tree stores:

- Current battle state
- Parent node
- Children nodes
- Move leading to the node
- Number of visits
- Number of wins

Example:

```text
ROOT
├── Fire Ball
│   ├── Heal
│   ├── Quick Attack
│   └── Strong Attack
│
├── Heal
│   ├── Fire Ball
│   ├── Heal
│   └── Quick Attack
│
└── Quick Attack
    ├── Heal
    ├── Fire Ball
    └── Strong Attack
```

### Selection

The algorithm chooses nodes using the UCT (Upper Confidence Bound for Trees) formula:

```
UCT = wins / visits +
      C * sqrt(ln(parent_visits) / visits)
```

This balances:

- Exploration of unexplored moves
- Exploitation of moves known to perform well

### Expansion

When a leaf node is reached:

- New child nodes are created
- Each child represents one possible move

### Rollout

After expansion, the algorithm performs a simulated battle.

Players continue making moves until:

- the player reaches 0 HP
- the enemy reaches 0 HP

The rollout returns:

- 1 for enemy victory
- 0 for enemy defeat

### Backpropagation

The rollout result is propagated back through the tree.

Each visited node updates:

- visit count
- win count

Over time the tree accumulates statistical knowledge about which decisions lead to victory.

### Advantages

Compared to Random AI:

- Evaluates future consequences
- Adapts to changing battle situations
- Uses probabilistic decision making
- Produces stronger opponents without manually written strategies

### Computational Complexity

The strength of the AI depends on the number of simulations.

Typical values used during development:

- 100 simulations – very fast
- 500 simulations – balanced
- 1000+ simulations – stronger but slower

The final version uses configurable simulation counts depending on desired difficulty.

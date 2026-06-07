# 🤖 Artificial Intelligence

Mount Carlos contains two enemy AI systems:

## Random AI

The basic AI chooses one of the available moves randomly.

This implementation was primarily used for testing and balancing the combat system.

---

## Monte Carlo Tree Search (MCTS)

The advanced AI uses a Monte Carlo Tree Search algorithm to determine the most promising move.

Unlike a simple rule-based opponent, the enemy attempts to predict the future outcome of a battle by simulating many possible combat sequences before making a decision.

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

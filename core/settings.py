from ai.simulation import RandomChoice, MonteCarloRolloutAI, CurrentBattleState
from ai.monte_carlo import MonteCarloAI

class Settings:
    def __init__(self, difficulty="medium"):
        self.difficulty = difficulty

    def get_engine(self, player, enemy):
        enemyAI = None
        if self.difficulty == "easy":
            enemyAI = RandomChoice(enemy.moves)
        elif self.difficulty == "medium":
            enemyAI = MonteCarloRolloutAI(player, enemy)
        elif self.difficulty == "hard":
            enemyAI = MonteCarloAI()
        
        return enemyAI

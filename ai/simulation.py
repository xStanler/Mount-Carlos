import numpy as np

class RandomChoice:
    def __init__(self, moves):
        self.moves = moves

    def chooseMove(self):
        rng = np.random.randint(len(self.moves))

        return self.moves[rng]

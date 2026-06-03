#Move class
class Move():
    def __init__(self, name: str = 'None', attack: int = 0, heal: int = 0, uses: int = 5):
        self.name = name
        self.attack = attack
        self.heal = heal
        self.uses = uses

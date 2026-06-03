import pygame
from engine.player import Move
from pathlib import Path
from enum import Enum
import numpy as np

class EnemyType(Enum):
    FIRE = 0
    WATER = 1
    GRASS = 2
    DRAGON = 3
    MYTHIC = 4
    EMPTY = 5

class EntitySprites:
    
    def __init__(self, enType):
        self.type = enType
        self.idle = []
        self.attack = []
        self.hurt = []
        self.idle_size = (0, 0)
        self.idle_len = 0
        self.attack_size = (0, 0)
        self.attack_len = 0
        self.hurt_size = (0, 0)
        self.hurt_len = 2
        typeName = ""

        match self.type:
            case EnemyType.FIRE:
                typeName = "Fire"
                self.attack_size = (56, 56)
                self.attack_len = 11

                self.idle_size = (40, 48)
                self.idle_len = 4

                self.hurt_size = (64, 64)
            case EnemyType.WATER:
                typeName = "Water"
                self.attack_size = (48, 56)
                self.attack_len = 6
                #Attack2
                # self.attack_size = (64, 72)
                # self.attack_len = 17

                self.idle_size = (40, 40)
                self.idle_len = 8

                self.hurt_size = (40, 40)
            case EnemyType.GRASS:
                typeName = "Grass"
                self.attack_size =(72, 72)
                self.attack_len = 11

                self.idle_size = (32, 32)
                self.idle_len = 4

                self.hurt_size = (48, 48)
            case EnemyType.DRAGON:
                typeName = "Dragon"
                self.attack_size = (48, 64)
                self.attack_len = 12

                # self.idle_size = (40, 64)
                # self.idle_len = 7
                self.idle_size = (48, 56)
                self.idle_len = 6

                self.hurt_size = (48, 72)
            case EnemyType.MYTHIC:
                typeName = "Mythic"
                self.attack_size = (80, 88)
                self.attack_len = 15

                self.idle_size = (32, 64)
                self.idle_len = 8

                self.hurt_size = (32, 48)
                self.hurt_len = 12

        spritePath = Path(__file__).parent.parent / f"assets/Enemies/{typeName}"

        currentFile = pygame.image.load(spritePath / "Attack.png").convert_alpha()
        for col in range(self.attack_len):
            rect = pygame.Rect(col*self.attack_size[0],
                               7 * self.attack_size[1],
                               *self.attack_size)
            sprite = currentFile.subsurface(rect).copy()
            sprite = pygame.transform.scale_by(sprite, 4)

            self.attack.append(sprite)
        
        currentFile = pygame.image.load(spritePath / "Idle.png").convert_alpha()
        for col in range(self.idle_len):
            rect = pygame.Rect(col*self.idle_size[0],
                               7 * self.idle_size[1],
                               *self.idle_size)
            sprite = currentFile.subsurface(rect).copy()
            sprite = pygame.transform.scale_by(sprite, 4)

            self.idle.append(sprite)

        currentFile = pygame.image.load(spritePath / "Hurt.png").convert_alpha()
        for col in range(self.hurt_len):
            rect = pygame.Rect(col*self.hurt_size[0],
                               7 * self.hurt_size[1],
                               *self.hurt_size)
            sprite = currentFile.subsurface(rect).copy()
            sprite = pygame.transform.scale_by(sprite, 4)

            self.hurt.append(sprite)
        
class Enemy:
    def __init__(self, name = "", enType = EnemyType.EMPTY):
        self.name = name
        if enType == EnemyType.EMPTY:
            rng = np.random.randint(5)
            
            match rng:
                case 0:
                    enType = EnemyType.FIRE
                case 1:
                    enType = EnemyType.WATER
                case 2:
                    enType = EnemyType.GRASS
                case 3:
                    enType = EnemyType.DRAGON
                case 4:
                    enType = EnemyType.MYTHIC
        self.type = enType
        self.health = 15 + np.random.randint(11)
        self.HEALTH = self.health
        self.moves = []
        self.sprites = EntitySprites(enType)

        self.animation_timer = 0
        self.animation_frame = 0
        #0 -> idle 1 -> attack 2 -> hurt
        self.state = 0

        self.make_moves()
        self.get_name()

    def get_name(self):
        names = ["Draco", "Bully", "Splassssh", "Executoner", "Franek", "Swiftie", "Szarik", "Reksio", "???"]

        self.name = names[np.random.randint(len(names))]

    def get_sprites(self):
        match self.state:
            case 0:
                return self.sprites.idle
            case 1:
                return self.sprites.attack
            case 2:
                return self.sprites.hurt

        return self.sprites.idle

    def make_moves(self):
        rand_dmg = 5 + np.random.randint(8)

        match self.type:
            case EnemyType.FIRE:
                self.moves.append(Move("Fire Ball", rand_dmg, 0, 2))
            case EnemyType.WATER:
                self.moves.append(Move("Water Canon", rand_dmg, 0, 2))
            case EnemyType.GRASS:
                self.moves.append(Move("Leaf Vines", rand_dmg, 0, 2))
            case EnemyType.DRAGON:
                self.moves.append(Move("Scorching Breath", rand_dmg, 0, 2))
            case EnemyType.MYTHIC:
                self.moves.append(Move("Almighty Help", rand_dmg, 0, 2))


        aviableMoves = [
                Move("Quick Attack", 1 + np.random.randint(3), 0, 20),
                Move("Heal", 0, 5, 4),
                Move("Boost Up", 0, 2 + np.random.randint(5), 5),
                Move("Strong Attack", 5 + np.random.randint(4), 0, 3),
                Move("Poison Ivy", 3*np.random.randint(4), (-2)*np.random.randint(3), 5),
                Move("Pass Turn", 0, 0, 30),
                Move("Self Exchaustion", 0, -2, 10),
                Move("Normal Attack", 2, 0, 20)
                ]

        for i in range(3):
            self.moves.append(aviableMoves[np.random.randint(len(aviableMoves))])

# if __name__ == "__main__":
#     screen = pygame.display.set_mode((100, 100), pygame.SCALED)
#     enemy = Enemy("Draco", EnemyType.MYTHIC)
#     clock = pygame.time.Clock()
#     anim = 0
#     animTimer = 0
#
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#
#         screen.fill((0, 200, 0))
#
#         animTimer += 1
#         if animTimer >= 10: 
#             animTimer = 0
#             anim = (anim + 1)%enemy.sprites.attack_len
#         screen.blit(enemy.sprites.attack[anim], (0, 0))
#
#         pygame.display.flip()
#         clock.tick(60)

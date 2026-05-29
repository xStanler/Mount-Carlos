import pygame
from pathlib import Path

class Move():
    def __init__(self, name: str = 'None', attack: int = 0, heal: int = 0, uses: int = 5):
        self.name = name
        self.attack = attack
        self.heal = heal
        self.uses = uses


class Player():
    def __init__(self, x: int = 5, y: int = 5):
        self.name = "Stanler"
        self.health = 20
        self.walking_speed = 3.0
        self.moves = []
        self.scale = 64

        self.create_moves()
        file = Path(__file__).resolve().parent.parent / "assets/Tiles/tile_0131.png"
        self.avatar = pygame.image.load(file).convert_alpha()
        self.avatar = pygame.transform.scale(self.avatar, (64, 64))

        self.x = x*self.scale 
        self.y = y*self.scale 

    def create_moves(self):
        self.moves.append(Move("Heal", 0, 5, 4))
        self.moves.append(Move("Quick Attack", 2, 0, 20))
        self.moves.append(Move("Strong Attack", 7, 0, 2))

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w] | keys[pygame.K_UP]:
            self.y -= self.walking_speed

        if keys[pygame.K_s] | keys[pygame.K_DOWN]:
            self.y += self.walking_speed

        if keys[pygame.K_a] | keys[pygame.K_LEFT]:
            self.x -= self.walking_speed

        if keys[pygame.K_d] | keys[pygame.K_RIGHT]:
            self.x += self.walking_speed

    def render(self, screen):
        screen.blit(self.avatar, (self.x, self.y))

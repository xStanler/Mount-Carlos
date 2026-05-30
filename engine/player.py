import pygame
from pathlib import Path

#Move class
class Move():
    def __init__(self, name: str = 'None', attack: int = 0, heal: int = 0, uses: int = 5):
        self.name = name
        self.attack = attack
        self.heal = heal
        self.uses = uses

#NOTE: Character Sprites class
class CharacterSprites:
    CELL_SIZE = 48
    ROWS = 6
    COLS = 6

    def __init__(self, path):
        self.sheet = pygame.image.load(path).convert_alpha()

        self.frames = []

        for row in range(self.ROWS):
            current_row = []

            for col in range(self.COLS):
                rect = pygame.Rect(
                        col * self.CELL_SIZE,
                        row * self.CELL_SIZE,
                        self.CELL_SIZE,
                        self.CELL_SIZE
                        )
                sprite = pygame.transform.scale_by(
                        self.sheet.subsurface(rect).copy(),
                        4
                        )

                current_row.append(sprite)

            self.frames.append(current_row)

        self.idle_down = self.frames[0]
        self.idle_right = self.frames[1]
        self.idle_up = self.frames[2]
        self.idle_left = [
                pygame.transform.flip(frame, True, False)
                for frame in self.idle_right
                ]

        self.walk_down = self.frames[3]
        self.walk_right = self.frames[4]
        self.walk_up = self.frames[5]
        self.walk_left = [
                pygame.transform.flip(frame, True, False)
                for frame in self.walk_right
                ]


#NOTE: Player() class
class Player():
    def __init__(self, x: int = 5, y: int = 5):
        self.name = "Carlos"
        self.health = 20
        self.walking_speed = 5 
        self.moves = []

        self.scale = 64
        self.mapX = 42
        self.mapY = 43

        self.create_moves()

        self.direction = "down"
        self.moving = False
        file = Path(__file__).parent.parent / "assets/Player/player.png"
        self.sprites = CharacterSprites(file)

        self.animation_frame = 0
        self.animation_timer = 0
        
        self.x = x*self.scale 
        self.y = y*self.scale 

    def create_moves(self):
        self.moves.append(Move("Heal", 0, 5, 4))
        self.moves.append(Move("Quick Attack", 2, 0, 20))
        self.moves.append(Move("Strong Attack", 7, 0, 2))

    def update(self):
        keys = pygame.key.get_pressed()
        self.moving = False

        if (keys[pygame.K_w] or keys[pygame.K_UP]) and (self.scale*2.5 < self.y - self.walking_speed):
            self.direction = "up"
            self.moving = True

            self.y -= self.walking_speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN] and (self.y + self.walking_speed < self.scale*(self.mapY - 1.5)):
            self.direction = "down"
            self.moving = True

            self.y += self.walking_speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT] and (self.scale*1.5 < self.x - self.walking_speed):
            self.direction = "left"
            self.moving = True

            self.x -= self.walking_speed

        if keys[pygame.K_d] or keys[pygame.K_RIGHT] and (self.x + self.walking_speed < self.scale*(self.mapX-1.5)):
            self.direction = "right"
            self.moving = True

            self.x += self.walking_speed

        self.animation_timer += 1

        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 6

    def current_sprite(self):
        if self.moving:

            match self.direction:
                case "down":
                    return self.sprites.walk_down[self.animation_frame]
                case "up":
                    return self.sprites.walk_up[self.animation_frame]
                case "right":
                    return self.sprites.walk_right[self.animation_frame]
                case "left":
                    return self.sprites.walk_left[self.animation_frame]
        else:

            match self.direction:
                case "down":
                    return self.sprites.idle_down[self.animation_frame]
                case "up":
                    return self.sprites.idle_up[self.animation_frame]
                case "right":
                    return self.sprites.idle_right[self.animation_frame]
                case "left":
                    return self.sprites.idle_left[self.animation_frame]
    
    def render(self, screen, camera):
        sprite = self.current_sprite()

        screen.blit(sprite, (int(self.x - camera.x - 96), int(self.y - camera.y - 96*1.5)))

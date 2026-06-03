from engine.map import TileType
from utils.move import Move
import pygame
from pathlib import Path
import numpy as np

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
    def __init__(self, x: int = 4, y: int = 4):
        self.name = "Carlos"
        self.health = 20
        self.HEALTH = self.health
        self.walking_speed = 5 
        self.moves = []
        self.scale = 64
        self.x = x*self.scale 
        self.y = y*self.scale*1.5 
        self.startPosX = self.x
        self.startPosY = self.y
        self.last_tile_x = None
        self.last_tile_y = None

        self.mapX = 42
        self.mapY = 43

        self.create_moves()
        self.in_battle = False

        self.direction = "down"
        self.moving = False
        file = Path(__file__).parent.parent / "assets/Player/player.png"
        self.sprites = CharacterSprites(file)

        self.animation_frame = 0
        self.animation_timer = 0

    @property
    def hitbox(self):
        hitbox_width = 32
        hitbox_height = 32

        return pygame.Rect(
                self.x - hitbox_width // 2,
                self.y - hitbox_height // 2,
                hitbox_width,
                hitbox_height
                )

    def create_moves(self):
        self.moves.append(Move("Healing Axe", 6, 3, 2))
        self.moves.append(Move("Heal", 0, 5, 4))
        self.moves.append(Move("Quick Attack", 2, 0, 20))
        self.moves.append(Move("Strong Attack", 7, 0, 3))

    def on_bush_collision(self):
        self.walking_speed = 1
        rng = np.random.randint(100)

        if (self.x != self.startPosX or self.y != self.startPosY) and rng < 50:
            print(f"{self.name} wszedł w krzak! Przygotuj się na walke??")
            self.in_battle = True

    def update_animation(self):
        self.animation_timer += 1

        if self.animation_timer >= 10:
            self.animation_timer = 0
            self.animation_frame = (self. animation_frame + 1) % 6

    def update(self, map):
        keys = pygame.key.get_pressed()
        self.moving = False
        tile_x = int(self.x // self.scale)
        tile_y = int(self.y // self.scale)

        dx = 0
        dy = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction = "up"
            self.moving = True

            dy -= self.walking_speed

        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction = "down"
            self.moving = True

            dy += self.walking_speed

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction = "left"
            self.moving = True

            dx -= self.walking_speed

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction = "right"
            self.moving = True

            dx += self.walking_speed

        if self.moving:
            self.x += dx
            current_hitbox = self.hitbox
            corners_x = [
                    (current_hitbox.left, current_hitbox.top),
                    (current_hitbox.right, current_hitbox.top),
                    (current_hitbox.left, current_hitbox.bottom),
                    (current_hitbox.right, current_hitbox.bottom)
                ]
            for cx, cy in corners_x:
                if map.is_solid_at_pixel(cx, cy):
                    self.x -= dx
                    break

        # Oś Y
            self.y += dy
            current_hitbox = self.hitbox
            corners_y = [
                (current_hitbox.left, current_hitbox.top),
                (current_hitbox.right, current_hitbox.top),
                (current_hitbox.left, current_hitbox.bottom),
                (current_hitbox.right, current_hitbox.bottom)
            ]
            for cx, cy in corners_y:
                if map.is_solid_at_pixel(cx, cy):
                    self.y -= dy
                    break

        if( tile_x != self.last_tile_x or tile_y != self.last_tile_y ):

            trigger_detected = map.check_trigger_at_pixel(self.x, self.y)
            if trigger_detected == TileType.BUSH: 
                self.on_bush_collision()
            else:
                self.walking_speed = 5

            self.last_tile_x = tile_x
            self.last_tile_y = tile_y

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

    def battle_sprite(self):
        return self.sprites.idle_right[self.animation_frame]
    
    def render(self, screen, camera):
        sprite = self.current_sprite()

        screen.blit(sprite, (int(self.x - camera.x - 96), int(self.y - camera.y - 96*1.5)))

        #WARNING: DEBUG HITBOX
        debug_rect = pygame.Rect(int(self.hitbox.x - camera.x), int(self.hitbox.y - camera.y), self.hitbox.width, self.hitbox.height)
        pygame.draw.rect(screen, (255, 0, 0), debug_rect, 2)

from engine.player import Player
from engine.enemy import Enemy
import pygame

class Battle:
    def __init__(self, player = Player(), enemy = Enemy()):
        self.player = player
        self.enemy = enemy

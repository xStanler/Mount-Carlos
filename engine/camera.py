# import pygame

class Camera():
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target, screen):
        self.x = target.x - screen.get_width() // 2
        self.y = target.y - screen.get_height() // 2


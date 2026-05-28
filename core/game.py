import pygame

class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((640, 640))
        self.clock = pygame.time.Clock()
        
        self.running = True
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()

        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def render(self):
        self.screen.fill("purple")
        pygame.display.flip()

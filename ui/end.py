from ui.menus import Button
import pygame
from pathlib import Path

class EndScreen:
    def __init__(self, screen):
        self.screen = screen

        font_path = Path(__file__).parent.parent / "assets/VT323-Regular.ttf"
        self.font = pygame.font.Font(str(font_path), 32)
        self.bigFont = pygame.font.Font(str(font_path), 72)

        btn_w, btn_h = 240, 50
        btn_x = (self.screen.get_size()[0] // 2) - (btn_w // 2)

        self.back_button = Button("WYJDŹ", btn_x, 500, btn_w, btn_h, (60, 83, 60), (51, 71, 51), self.font)

        self.textLine = "Koniec gry!"

    def update(self, mouse_pos, mouse_clicked):
        self.back_button.update(mouse_pos)

        if self.back_button.is_clicked(mouse_pos, mouse_clicked):
            return "QUIT"

        return "NONE"

    def render(self, screen):
        self.back_button.set_position((screen.get_size()[0] // 2) - (240 // 2), self.screen.get_size()[1] - 150)

        screen.fill((102, 122, 143))

        text = self.bigFont.render(
                    self.textLine,
                    True,
                    (200, 200, 200)
                    )

        rect = text.get_rect( center=(screen.get_width() // 2, 120) )
        screen.blit(text, rect)

        self.back_button.draw(screen)

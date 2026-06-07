from ui.menus import Button
import pygame
from pathlib import Path

class HowToPlay:
    def __init__(self, screen):
        self.screen = screen

        font_path = Path(__file__).parent.parent / "assets/VT323-Regular.ttf"
        self.font = pygame.font.Font(str(font_path), 32)

        btn_w, btn_h = 240, 50
        btn_x = (self.screen.get_size()[0] // 2) - (btn_w // 2)

        self.back_button = Button("POWRÓT", btn_x, 500, btn_w, btn_h, (60, 83, 60), (51, 71, 51), self.font)

        self.lines = [
    "Witam w grze Mount Carlos!",
    "",
    "Przyciskami W, S, A, D lub strzałkami",
    "poruszasz się postacią.",
    "Celem gry jest walka z przeciwnikami",
    "znajdującymi się w krzakach.",
    "Walka odbywa się w systemie turowym.",
    "Aby wybrać atak gracza,",
    "należy wcisnąć odpowiadający",
    "ruchowi klawisz 1-4.",
    "Po każdej wiadomości",
    "należy wcisnąć ENTER.",
    "Powodzenia!"
]

        # print("Witam w grze Monut Carlos!\nPrzyciskami W, S, A, D lub strzałkami poruszasz się postacią.\nCelem gry jest walka z przeciwnikami znajdującymi sie w krzakach!\nWalka odbywa się w systemie turowym. Aby wybrać atak gracza, nalezy wcisnąć odpowiadający danemu ruchowi przycisk 1-4. Po każdej wiadomości wyświetlanej na ekrani, należy wcisnąć ENTER, aby kontynuować!!!\nPowodzenia, miłego grania")

    def update(self, mouse_pos, mouse_clicked):
        self.back_button.update(mouse_pos)

        if self.back_button.is_clicked(mouse_pos, mouse_clicked):
            return "BACK"

        return "NONE"

    def render(self, screen):
        self.back_button.set_position((screen.get_size()[0] // 2) - (240 // 2), self.screen.get_size()[1] - 150)

        screen.fill((102, 122, 143))

        y = 50
        for line in self.lines:
            text = self.font.render(
                    line,
                    True,
                    (200, 200, 200)
                    )

            rect = text.get_rect( center=(screen.get_width() // 2, y) )
            screen.blit(text, rect)
            y += 35
        self.back_button.draw(screen)

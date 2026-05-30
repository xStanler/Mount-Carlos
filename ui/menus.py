import pygame
import sys

class Button:
    def __init__(self, text, x, y, width, height, base_color, hover_color, font):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.base_color = base_color
        self.hover_color = hover_color
        self.font = font
        self.current_color = self.base_color

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.base_color

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, mouse_pos, mouse_up_event):
        return self.rect.collidepoint(mouse_pos) and mouse_up_event

class MainMenu():
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.title_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.button_font = pygame.font.SysFont("arial", 20)

        btn_w, btn_h = 240, 50
        btn_x = (screen_width // 2) - (btn_w // 2)

        self.start_button = Button("ROZPOCZNIJ GRĘ", btn_x, 250, btn_w, btn_h, (40, 50, 70), (60, 80, 110), self.button_font)
        self.quit_button = Button("WYJDŹ", btn_x, 330, btn_w, btn_h, (40, 50, 70), (150, 50, 50), self.button_font)

        self.title_surf = self.title_font.render("MOUNT CARLOS", True, (255, 215, 0))
        self.title_rect = self.title_surf.get_rect(center=(screen_width // 2, 120))

    def update(self, mouse_pos, mouse_clicked):
        self.start_button.update(mouse_pos)
        self.quit_button.update(mouse_pos)

        if self.start_button.is_clicked(mouse_pos, mouse_clicked):
            return "START"
        if self.quit_button.is_clicked(mouse_pos, mouse_clicked):
            return "QUIT"

        return "NONE"

    def render(self, screen):
        screen.fill((20, 20, 30))

        screen.blit(self.title_surf, self.title_rect)
        self.start_button.draw(screen)
        self.quit_button.draw(screen)

from ai.simulation import RandomChoice, MonteCarloRolloutAI, CurrentBattleState
from ai.monte_carlo import MonteCarloAI
from ui.menus import Button
import pygame
from pathlib import Path

class Settings:
    def __init__(self, screen, difficulty="medium"):
        self.screen = screen
        self.difficulty = difficulty

        font_path = Path(__file__).parent.parent / "assets/VT323-Regular.ttf"
        self.button_font = pygame.font.Font(str(font_path), 32)

        btn_w, btn_h = 240, 50
        btn_x = (self.screen.get_size()[0] // 2) - (btn_w // 2)
        self.easy_button = Button("ŁATWY", btn_x, 250, btn_w, btn_h, (60, 83, 60), (51, 71, 51), self.button_font)
        self.medium_button = Button("ŚREDNI", btn_x, 330, btn_w, btn_h, (60, 83, 60), (51, 71, 51), self.button_font)
        self.hard_button = Button("TRUDNY", btn_x, 410, btn_w, btn_h, (60, 83, 60), (51, 71, 51), self.button_font)

    def get_engine(self, player, enemy):
        enemyAI = None
        if self.difficulty == "easy":
            enemyAI = RandomChoice(enemy.moves)
        elif self.difficulty == "medium":
            enemyAI = MonteCarloRolloutAI(player, enemy)
        elif self.difficulty == "hard":
            currState = CurrentBattleState(
                    player.health,
                    enemy.health,
                    player.moves,
                    enemy.moves,
                    False
                    )

            enemyAI = MonteCarloAI(currState)
        
        return enemyAI

    def update(self, mouse_pos, mouse_clicked):
        self.easy_button.update(mouse_pos)
        self.medium_button.update(mouse_pos)
        self.hard_button.update(mouse_pos)

        if self.easy_button.is_clicked(mouse_pos, mouse_clicked):
            self.difficulty = "easy"
            return True
        if self.medium_button.is_clicked(mouse_pos, mouse_clicked):
            self.difficulty = "medium"
            return True
        if self.hard_button.is_clicked(mouse_pos, mouse_clicked):
            self.difficulty = "hard"
            return True

        return False

    def render(self, screen):
        self.screen_width, self.screen_height = screen.get_size()
        self.easy_button.set_position((self.screen_width // 2) - (240 // 2), 250)
        self.medium_button.set_position((self.screen_width // 2) - (240 // 2), 330)
        self.hard_button.set_position((self.screen_width // 2) - (240 // 2), 410)

        screen.fill((102, 122, 143))
        self.easy_button.draw(screen)
        self.medium_button.draw(screen)
        self.hard_button.draw(screen)

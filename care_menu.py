import pygame
from typing import List, Tuple, Optional

class CareMenu:
    def __init__(self, screen_width: int, screen_height: int):
        self.width = screen_width
        self.height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.active = False
        self.current_options: List[str] = []
        self.option_rects: List[pygame.Rect] = []
        self.menu_type: Optional[str] = None

        # Menu types and their options
        self.menu_options = {
            "food": ["hamburger", "hot dog", "nachos"],
            "whiskey": ["large", "extra large"],
            "play": [
                "Prank call another GM",
                "Beg Troy Aikman to coach the team",
                "Pretend you're not racist",
                "Ask Coach Prime to return"
            ]
        }

    def show_menu(self, menu_type: str):
        self.active = True
        self.menu_type = menu_type
        self.current_options = self.menu_options[menu_type]
        self._create_option_rects()

    def hide_menu(self):
        self.active = False
        self.current_options = []
        self.option_rects = []
        self.menu_type = None

    def _create_option_rects(self):
        self.option_rects = []
        option_height = 50
        total_height = len(self.current_options) * (option_height + 10)
        start_y = (self.height - total_height) // 2

        for i, option in enumerate(self.current_options):
            rect = pygame.Rect(
                self.width // 4,
                start_y + i * (option_height + 10),
                self.width // 2,
                option_height
            )
            self.option_rects.append(rect)

    def draw(self, screen: pygame.Surface):
        if not self.active:
            return

        # Draw semi-transparent background
        overlay = pygame.Surface((self.width, self.height))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        screen.blit(overlay, (0, 0))

        # Draw options
        for i, (option, rect) in enumerate(zip(self.current_options, self.option_rects)):
            pygame.draw.rect(screen, (255, 255, 255), rect)
            text = self.font.render(option, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    def handle_click(self, pos: Tuple[int, int]) -> Optional[str]:
        if not self.active:
            return None

        for option, rect in zip(self.current_options, self.option_rects):
            if rect.collidepoint(pos):
                self.hide_menu()
                return option

        return None

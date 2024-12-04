import pygame
from typing import Dict, Tuple, Optional, List
from menu_config import MENU_STRUCTURE

class UIManager:
    def __init__(self, screen_width: int, screen_height: int):
        self.width = screen_width
        self.height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.colors = {
            "white": (255, 255, 255),
            "black": (0, 0, 0),
            "green": (0, 255, 0),
            "red": (255, 0, 0),
            "yellow": (255, 255, 0),
            "gray": (128, 128, 128)
        }

        # Menu state
        self.current_menu = "main"
        self.menu_stack = []

        # Button layout
        button_width = 200
        button_height = 50
        button_y = screen_height - 70
        spacing = (screen_width - (3 * button_width)) // 4

        # Create button positions
        self.button_positions = []
        for i in range(3):
            self.button_positions.append(
                pygame.Rect(
                    spacing + (i * (button_width + spacing)),
                    button_y,
                    button_width,
                    button_height
                )
            )

        # Status areas
        self.status_area = pygame.Rect(50, 50, screen_width - 100, 40)
        self.message_area = pygame.Rect(50, 100, screen_width - 100, 40)
        self.vitals_area = pygame.Rect(50, 150, screen_width - 100, 100)

        self.current_status = ""
        self.current_message = ""
        self.vitals = {"hunger": 100, "thirst": 100, "energy": 100, "happiness": 100}

    def draw(self, screen: pygame.Surface):
        # Draw vitals and status
        self.draw_status(screen)

        # Get current menu buttons
        menu_info = MENU_STRUCTURE[self.current_menu]
        buttons = menu_info["buttons"]
        descriptions = menu_info["descriptions"]

        # Draw up to 3 buttons
        for i, (button, desc, pos) in enumerate(zip(buttons, descriptions, self.button_positions)):
            self.draw_menu_button(screen, button, desc, pos)

        # Draw back button if in submenu
        if self.menu_stack:
            self.draw_back_button(screen)

    def draw_menu_button(self, screen: pygame.Surface, text: str, description: str, rect: pygame.Rect):
        # Draw button
        pygame.draw.rect(screen, self.colors["green"], rect)

        # Draw button text
        text_surf = self.font.render(text[:15] + "..." if len(text) > 15 else text, True, self.colors["black"])
        text_rect = text_surf.get_rect(center=rect.center)
        screen.blit(text_surf, text_rect)

        # Draw tooltip on hover
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            self.draw_tooltip(screen, description, mouse_pos)

    def draw_back_button(self, screen: pygame.Surface):
        back_button = pygame.Rect(10, 10, 100, 40)
        pygame.draw.rect(screen, self.colors["gray"], back_button)
        text = self.small_font.render("Back", True, self.colors["black"])
        text_rect = text.get_rect(center=back_button.center)
        screen.blit(text, text_rect)

    def handle_click(self, pos: Tuple[int, int]) -> Optional[Tuple[str, str]]:
        # Check back button
        if self.menu_stack and self.back_button.collidepoint(pos):
            self.current_menu = self.menu_stack.pop()
            return None

        # Check menu buttons
        buttons = MENU_STRUCTURE[self.current_menu]["buttons"]
        for button, rect in zip(buttons, self.button_positions):
            if rect.collidepoint(pos):
                if self.current_menu in MENU_STRUCTURE and button in MENU_STRUCTURE:
                    self.menu_stack.append(self.current_menu)
                    self.current_menu = button.lower()
                return (self.current_menu, button)

        return None

    def draw_tooltip(self, screen: pygame.Surface, text: str, pos: Tuple[int, int]):
        tooltip_surf = self.small_font.render(text, True, self.colors["black"])
        tooltip_rect = tooltip_surf.get_rect(topleft=(pos[0] + 10, pos[1] - 30))

        # Draw background
        padding = 5
        bg_rect = tooltip_rect.inflate(padding * 2, padding * 2)
        pygame.draw.rect(screen, self.colors["white"], bg_rect)
        pygame.draw.rect(screen, self.colors["black"], bg_rect, 1)

        screen.blit(tooltip_surf, tooltip_rect)

    def update_status(self, status: str):
        self.current_status = status

    def update_message(self, message: str):
        self.current_message = message

    def update_vitals(self, hunger: float, thirst: float, energy: float, happiness: float):
        self.vitals = {
            "hunger": hunger,
            "thirst": thirst,
            "energy": energy,
            "happiness": happiness
        }

    def draw_status(self, screen: pygame.Surface):
        # Draw game time and status
        status_text = self.font.render(self.current_status, True, self.colors["black"])
        screen.blit(status_text, self.status_area)

        # Draw current message
        if self.current_message:
            message_text = self.font.render(self.current_message, True, self.colors["black"])
            screen.blit(message_text, self.message_area)

        # Draw vitals bars
        bar_height = 20
        bar_spacing = 25
        for i, (vital, value) in enumerate(self.vitals.items()):
            y_pos = self.vitals_area.top + (i * bar_spacing)

            # Draw label
            label = self.small_font.render(f"{vital.capitalize()}: {int(value)}%", True, self.colors["black"])
            screen.blit(label, (self.vitals_area.left, y_pos))

            # Draw bar background
            bar_bg = pygame.Rect(self.vitals_area.left + 120, y_pos + 5, 200, bar_height)
            pygame.draw.rect(screen, self.colors["black"], bar_bg, 1)

            # Draw bar fill
            bar_fill = pygame.Rect(bar_bg.left, bar_bg.top, bar_bg.width * (value / 100), bar_height)
            color = self._get_status_color(value)
            pygame.draw.rect(screen, color, bar_fill)

    def _get_status_color(self, value: float) -> Tuple[int, int, int]:
        if value > 70:
            return self.colors["green"]
        elif value > 30:
            return self.colors["yellow"]
        else:
            return self.colors["red"]

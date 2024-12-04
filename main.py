import pygame
import sys
from datetime import datetime
from game_state import GameState
from event_manager import EventManager
from ui_manager import UIManager
from config import GAME_CONFIG, MESSAGES
from time_manager import TimeManager
from menu_config import MENU_STRUCTURE, BUTTON_STATES
import random

class JerryGame:
    def __init__(self):
        print("Initializing Jerry Jones Simulator...")
        pygame.init()

        # Set SDL environment variables for container compatibility
        import os
        os.environ['SDL_VIDEODRIVER'] = 'x11'
        os.environ['SDL_AUDIODRIVER'] = 'dummy'

        # Initialize display with robust error handling for containerized environment
        try:
            pygame.display.init()
        except pygame.error as e:
            print(f"Error: Display initialization failed: {e}")
            print("Checking display environment...")
            print(f"DISPLAY={os.environ.get('DISPLAY', 'Not set')}")
            print(f"SDL_VIDEODRIVER={os.environ.get('SDL_VIDEODRIVER', 'Not set')}")
            sys.exit(1)

        self.width = GAME_CONFIG["SCREEN_WIDTH"]
        self.height = GAME_CONFIG["SCREEN_HEIGHT"]

        try:
            # Force software rendering for better container compatibility
            os.environ['SDL_RENDERER_DRIVER'] = 'software'
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Jerry Jones Simulator")
        except pygame.error as e:
            print(f"Error: Could not set video mode: {e}")
            sys.exit(1)

        self.state = GameState()
        self.event_manager = EventManager()
        self.ui_manager = UIManager(self.width, self.height)
        self.clock = pygame.time.Clock()
        self.time_manager = TimeManager()
        self.current_message = ""
        self.game_state = GAME_CONFIG["STATES"]["PLAYING"]
        print("Game initialized successfully")

    def run(self):
        print("Starting game loop...")
        while True:
            try:
                self.handle_events()
                self.update()
                self.draw()
                self.clock.tick(GAME_CONFIG["FPS"])
            except Exception as e:
                print(f"Error in game loop: {str(e)}")
                raise

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                result = self.ui_manager.handle_click(event.pos)
                if result:
                    menu_type, option = result
                    self.handle_menu_action(menu_type, option)

    def handle_menu_action(self, menu_type: str, option: str):
        if menu_type == "main":
            if option == "Care":
                if self.state.should_sleep():
                    self.ui_manager.current_menu = "sleep_time"
                else:
                    self.ui_manager.current_menu = "care"
            elif option == "Play" and not self.state.is_sleeping:
                self.ui_manager.current_menu = "play"
            elif option == "Scold" and self.state.last_bad_decision and \
                 self.time_manager.get_minutes_passed(self.state.last_bad_decision) < 30:
                self.ui_manager.current_menu = "bad_decision"

        elif menu_type == "care":
            if option == "Food":
                self.ui_manager.current_menu = "food"
            elif option == "Whiskey":
                self.ui_manager.current_menu = "whiskey"
            elif option == "Sleep":
                self.state.sleep()
                self.ui_manager.current_menu = "main"

        elif menu_type == "food":
            self.state.feed(option.lower())
            if random.random() < 0.2:  # 20% chance for reward
                self.state.give_reward("dancer")
            self.ui_manager.current_menu = "main"

        elif menu_type == "whiskey":
            size = "extra large" if option == "Extra Large Whiskey" else "large"
            self.state.give_whiskey(size)
            if random.random() < 0.2:
                self.state.give_reward("glass of whiskey")
            self.ui_manager.current_menu = "main"

        elif menu_type == "play":
            play_actions = {
                "Prank GM Call": "Prank call another GM",
                "Beg Aikman": "Beg Troy Aikman to coach",
                "Ask Prime": "Ask Coach Prime to return"
            }
            self.state.play(play_actions[option])
            if random.random() < 0.3:
                self.state.give_reward(random.choice(["dancer", "glass of whiskey"]))
            self.ui_manager.current_menu = "main"

        elif menu_type == "sleep_time":
            if option == "Sleep Now":
                self.state.sleep()
            self.ui_manager.current_menu = "main"

        elif menu_type == "bad_decision":
            if option == "Scold":
                self.state.scold()
            self.ui_manager.current_menu = "main"

    def update(self):
        try:
            if not self.state.is_alive:
                print("Game over - Jerry is no longer with us")
                self.game_state = GAME_CONFIG["STATES"]["GAME_OVER"]
                self.current_message = MESSAGES["GAME_OVER"]
                return

            self.state.update()

            # Update UI with current stats
            stats = {
                "hunger": self.state.hunger,
                "thirst": self.state.thirst,
                "energy": self.state.energy,
                "happiness": self.state.happiness
            }
            print(f"Current stats: {stats}")
            self.ui_manager.update_vitals(**stats)

            # Get any new messages
            new_message = self.state.get_next_message()
            if new_message:
                self.current_message = new_message

            # Update status display
            game_time = self.time_manager.format_game_time()
            status = f"Time: {game_time}"
            self.ui_manager.update_status(status)
            self.ui_manager.update_message(self.current_message)

        except Exception as e:
            print(f"Error in update: {str(e)}")
            raise

    def draw(self):
        try:
            self.screen.fill((255, 255, 255))
            self.ui_manager.draw(self.screen)
            pygame.display.flip()
        except Exception as e:
            print(f"Error in draw: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        game = JerryGame()
        game.run()
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

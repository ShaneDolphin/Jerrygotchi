from datetime import datetime
from time_manager import TimeManager
import random

class GameState:
    def __init__(self):
        self.last_fed = None
        self.last_whiskey = None
        self.last_bad_decision = None
        self.last_sleep = None
        self.last_reward = None
        self.is_sleeping = False
        self.is_alive = True
        self.hunger = 100
        self.thirst = 100
        self.energy = 100
        self.happiness = 100
        self.current_action = None
        self.message_queue = []
        self.time_manager = TimeManager()
        self.bad_decision_cooldown = 0

    def update(self):
        if not self.is_alive:
            return

        game_time = self.time_manager.get_game_time()

        # Update vitals based on accelerated time
        if self.last_fed:
            minutes_since_fed = self.time_manager.get_minutes_passed(self.last_fed)
            self.hunger = max(0, 100 - (minutes_since_fed / 60))  # Slower hunger drain
        else:
            self.hunger = max(0, self.hunger - 0.05)  # Small drain if never fed

        if self.last_whiskey:
            minutes_since_whiskey = self.time_manager.get_minutes_passed(self.last_whiskey)
            self.thirst = max(0, 100 - (minutes_since_whiskey / 60))  # Slower thirst drain
        else:
            self.thirst = max(0, self.thirst - 0.05)  # Small drain if never given whiskey

        if not self.is_sleeping:
            self.energy = max(0, self.energy - 0.02)  # Much slower energy drain
        else:
            sleep_minutes = self.time_manager.get_minutes_passed(self.last_sleep)
            if sleep_minutes >= random.randint(480, 540):  # Sleep duration check
                self.wake_up()
            else:
                self.energy = min(100, self.energy + 0.5)  # Slower energy recovery

        # Random events based on accelerated time
        if not self.is_sleeping:
            if self.last_bad_decision:
                minutes_since_bad = self.time_manager.get_minutes_passed(self.last_bad_decision)
                if minutes_since_bad >= random.randint(60, 240) and self.bad_decision_cooldown <= 0:
                    self.trigger_bad_decision()

            # Random reward chance
            if random.random() < 0.001:  # Reduced chance per update with accelerated time
                self.give_reward(random.choice(["dancer", "glass of whiskey"]))

        # Check if Jerry dies
        if self.hunger <= 0 or self.thirst <= 0 or self.energy <= 0:
            self.is_alive = False
            print(f"Jerry died! Stats: Hunger={self.hunger:.1f}, Thirst={self.thirst:.1f}, Energy={self.energy:.1f}")

    def trigger_bad_decision(self):
        bad_decisions = [
            "trading a key player",
            "drafting a worthless prospect",
            "promising a Super Bowl",
            "overpaying an old player"
        ]
        self.make_bad_decision(random.choice(bad_decisions))
        self.bad_decision_cooldown = 60  # Cooldown in game minutes

    def should_sleep(self) -> bool:
        game_time = self.time_manager.get_game_time()
        hour = game_time.hour
        return 21 <= hour <= 23 and not self.is_sleeping

    def feed(self, food_type: str):
        self.last_fed = datetime.now()
        self.hunger = 100
        self.happiness = min(100, self.happiness + 10)
        self.message_queue.append(f"Jerry enjoyed his {food_type}")

    def give_whiskey(self, size: str):
        self.last_whiskey = datetime.now()
        self.thirst = 100
        self.happiness = min(100, self.happiness + 15)
        self.message_queue.append(f"Jerry enjoyed his {size} whiskey")

    def sleep(self):
        if not self.is_sleeping:
            self.is_sleeping = True
            self.last_sleep = datetime.now()
            self.message_queue.append("Jerry went to sleep")

    def wake_up(self):
        if self.is_sleeping:
            self.is_sleeping = False
            self.energy = 100
            self.message_queue.append("I have soiled myself, but if you tell anyone, I'll never take us to the Super Bowl again.")

    def make_bad_decision(self, decision: str):
        self.last_bad_decision = datetime.now()
        self.happiness = max(0, self.happiness - 20)
        self.message_queue.append(f"Jerry made a bad decision: {decision}")

    def give_reward(self, reward: str):
        self.last_reward = datetime.now()
        self.happiness = min(100, self.happiness + 25)
        self.message_queue.append(f"Jerry got a reward: {reward}")

    def scold(self):
        self.happiness = max(0, self.happiness - 15)
        self.message_queue.append("Jerry has been scolded")

    def play(self, activity: str):
        self.happiness = min(100, self.happiness + 20)
        self.message_queue.append(f"Jerry had fun {activity}")

    def get_next_message(self) -> str:
        return self.message_queue.pop(0) if self.message_queue else ""

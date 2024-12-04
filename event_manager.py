from datetime import datetime, time
import random
from typing import Optional, Tuple

class EventManager:
    def __init__(self):
        self.events = {}
        self.rewards = ["dancer", "glass of whiskey"]

    def check_time_window(self, start_hour: int, end_hour: int) -> bool:
        current_time = datetime.now().time()
        start = time(start_hour, 0)
        end = time(end_hour, 0)
        return start <= current_time <= end

    def should_trigger_event(self, last_time: Optional[datetime], min_minutes: int, max_minutes: int) -> bool:
        if not last_time:
            return True
        interval = random.randint(min_minutes, max_minutes)
        time_passed = (datetime.now() - last_time).total_seconds() / 60
        return time_passed >= interval

    def get_food_event(self) -> Tuple[str, str]:
        options = ["hamburger", "hot dog", "nachos"]
        return "food", random.choice(options)

    def get_whiskey_event(self) -> Tuple[str, str]:
        options = ["large", "extra large"]
        return "whiskey", random.choice(options)

    def get_bad_decision_event(self) -> Tuple[str, str]:
        options = [
            "trading a key player",
            "drafting a worthless prospect",
            "promising a Super Bowl",
            "overpaying an old player"
        ]
        return "bad_decision", random.choice(options)

    def get_play_event(self) -> Tuple[str, str]:
        options = [
            "Prank call another GM",
            "Beg Troy Aikman to coach the team",
            "Pretend you're not racist",
            "Ask Coach Prime to return"
        ]
        return "play", random.choice(options)

    def get_reward(self) -> str:
        return random.choice(self.rewards)

    def should_sleep(self) -> bool:
        return self.check_time_window(21, 23)

    def calculate_sleep_duration(self) -> int:
        return random.randint(480, 540)

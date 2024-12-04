import time
from datetime import datetime, timedelta

class TimeManager:
    def __init__(self, acceleration_factor: float = 60.0):  # 1 minute = 1 second (changed from 1 hour = 1 second)
        self.acceleration_factor = acceleration_factor
        self.game_start_time = datetime.now()
        self.real_start_time = time.time()

    def get_game_time(self) -> datetime:
        real_seconds_passed = time.time() - self.real_start_time
        game_seconds_passed = real_seconds_passed * self.acceleration_factor
        return self.game_start_time + timedelta(seconds=game_seconds_passed)

    def get_minutes_passed(self, last_time: datetime) -> float:
        if not last_time:
            return float('inf')
        game_time = self.get_game_time()
        return (game_time - last_time).total_seconds() / 60

    def format_game_time(self) -> str:
        game_time = self.get_game_time()
        return game_time.strftime("%I:%M %p")

    def reset(self):
        self.game_start_time = datetime.now()
        self.real_start_time = time.time()

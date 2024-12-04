from datetime import time

GAME_CONFIG = {
    # Screen settings
    "SCREEN_WIDTH": 800,
    "SCREEN_HEIGHT": 600,
    "FPS": 60,

    # Time intervals (in minutes)
    "FOOD_INTERVAL": {
        "MIN": 60,
        "MAX": 360
    },
    "WHISKEY_INTERVAL": {
        "MIN": 45,
        "MAX": 450
    },
    "BAD_DECISION_INTERVAL": {
        "MIN": 60,
        "MAX": 240
    },
    "SLEEP_DURATION": {
        "MIN": 480,
        "MAX": 540
    },

    # Sleep schedule
    "SLEEP_WINDOW": {
        "START": time(21, 0),  # 9 PM
        "END": time(23, 0)     # 11 PM
    },

    # Game states
    "STATES": {
        "MENU": "menu",
        "PLAYING": "playing",
        "SLEEPING": "sleeping",
        "GAME_OVER": "game_over"
    }
}

# Messages
MESSAGES = {
    "WAKE_UP": "I have soiled myself, but if you tell anyone, I'll never take us to the Super Bowl again.",
    "NEED_SLEEP": "Jerry looks tired. Maybe it's time for bed?",
    "GAME_OVER": "Jerry has passed away. The Cowboys will never win another Super Bowl.",
    "REWARD": "Jerry got a reward! {}",
    "BAD_DECISION": "Jerry made a bad decision: {}",
}

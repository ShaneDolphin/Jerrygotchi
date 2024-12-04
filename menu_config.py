# Menu configuration to ensure we never show more than 3 buttons
MENU_STRUCTURE = {
    "main": {
        "buttons": ["Care", "Play", "Scold"],
        "descriptions": [
            "Take care of Jerry's needs",
            "Play with Jerry",
            "Scold Jerry for bad decisions"
        ]
    },
    "care": {
        "buttons": ["Food", "Whiskey", "Sleep"],
        "descriptions": [
            "Feed Jerry when he's hungry",
            "Give Jerry a drink when he's thirsty",
            "Put Jerry to bed (9PM-11PM)"
        ]
    },
    "food": {
        "buttons": ["Hamburger", "Hot Dog", "Nachos"],
        "descriptions": [
            "Give Jerry a hamburger",
            "Give Jerry a hot dog",
            "Give Jerry some nachos"
        ]
    },
    "whiskey": {
        "buttons": ["Large Whiskey", "Extra Large Whiskey"],
        "descriptions": [
            "Pour Jerry a large whiskey",
            "Pour Jerry an extra large whiskey"
        ]
    },
    "play": {
        "buttons": [
            "Prank GM Call",
            "Beg Aikman",
            "Ask Prime"
        ],
        "descriptions": [
            "Prank call another GM",
            "Beg Troy Aikman to coach the team",
            "Ask Coach Prime to return"
        ]
    }
}

# Messages for different game states
BUTTON_STATES = {
    "sleep_time": {
        "buttons": ["Sleep Now", "Stay Up", "Cancel"],
        "descriptions": [
            "Put Jerry to bed",
            "Keep Jerry awake a bit longer",
            "Go back to main menu"
        ]
    },
    "bad_decision": {
        "buttons": ["Scold", "Ignore", "Cancel"],
        "descriptions": [
            "Scold Jerry for his bad decision",
            "Let it slide this time",
            "Go back to main menu"
        ]
    }
}

# Validation to ensure no menu has more than 3 buttons
for menu in list(MENU_STRUCTURE.values()) + list(BUTTON_STATES.values()):
    if len(menu["buttons"]) > 3:
        raise ValueError("Menu cannot have more than 3 buttons")
    if len(menu["buttons"]) != len(menu["descriptions"]):
        raise ValueError("Each button must have a description")

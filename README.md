# Jerry Jones Simulator

A Tamagotchi-style game featuring Jerry Jones, where your goal is to keep him alive and well.

## Features

- Simple three-button interface
- Time-based events and needs management
- Random events and rewards
- Containerized for easy deployment

## Game Mechanics

- Feed Jerry (intervals: 60-360 minutes)
  - Options: hamburgers, hot dogs, nachos
- Give Jerry whiskey (intervals: 45-450 minutes)
  - Options: large or extra large portions
- Manage Jerry's sleep schedule (9PM-11PM)
- Handle Jerry's bad decisions
- Play with Jerry through various activities

## Requirements

- Docker
- Docker Compose

## Running the Game

1. Clone the repository
2. Navigate to the game directory
3. Run:
```bash
sudo docker compose up
```

## Controls

The game features a simple three-button interface:
1. Care (Food/Whiskey/Sleep)
2. Play
3. Scold

## Game Events

- Jerry needs regular feeding and whiskey
- Jerry makes bad decisions that need scolding
- Jerry needs sleep every night
- Random rewards (dancers or whiskey)
- Special messages and events

## Time Management

The game uses accelerated time:
- 1 real second = 1 game minute
- Events occur at random intervals within specified ranges
- Sleep cycle follows in-game time

## Troubleshooting

If you encounter display issues:
1. Ensure X11 is properly configured
2. Check that the DISPLAY environment variable is set
3. Verify Docker has proper permissions

## Technical Details

- Built with Python and Pygame
- Containerized with Docker
- Uses X11 for display
- Implements proper cleanup and error handling

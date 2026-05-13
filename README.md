# Pico Gamer

Pico Gamer is a revived MicroPython game console for Raspberry Pi Pico-class boards. It runs a menu of tiny 128x64 OLED games with six buttons, configurable pins, shared input/audio helpers, and a roadmap for adding many more games.

## Hardware Defaults

| Part | Default |
| --- | --- |
| Display | SSD1306 128x64 I2C, address `0x3C` |
| I2C | Bus 1, SDA GP14, SCL GP15 |
| Buttons | Up GP2, Down GP3, Left GP4, Right GP5, A GP6, B GP7 |
| Audio | PWM buzzer on GP18 |

Edit `config.py` to change pins or display settings.

## Current Games

| Game | Category | Notes |
| --- | --- | --- |
| Pong | Arcade | Paddle/ball game with stable speed and restart/menu flow |
| Snake | Arcade | Frame-loop snake with score and clean exit |
| Invaders | Arcade | Simplified Space Invaders |
| Dino | Runner | Jump/duck runner with lives |
| 2048 | Puzzle | Sliding tile puzzle |
| Tetris | Puzzle | Falling-block puzzle with mute support |
| Full Speed | Racing | Tiny road racer |
| Lunar Module | Skill | Fuel-and-velocity landing game |

## Planned Games

First batch: Breakout, Minefield, Sokoban, Lights Out, Sliding Puzzle.

Backlog: Flappy Pico, Asteroids Lite, Maze Runner, Frogger Micro, Dodge Rain, Tunnel Racer, Space Duel, Brick Drop, Micro Golf, Jetpack, Memory Match, Simon, Yahtzee Lite, Connect Four, Reversi Mini, Mastermind, Nonogram Tiny, Word Guess, Box Push, Tower Builder.

## Install With `mpremote`

Install MicroPython on the Pico first, then copy the project files:

```sh
python3 -m pip install mpremote
mpremote connect auto fs cp *.py :
mpremote connect auto fs mkdir DinoGame
mpremote connect auto fs cp DinoGame/*.py :DinoGame/
mpremote connect auto fs mkdir P2048
mpremote connect auto fs cp P2048/*.py :P2048/
mpremote connect auto fs mkdir TetrisGame
mpremote connect auto fs cp TetrisGame/*.py :TetrisGame/
mpremote connect auto reset
```

The launcher starts from `main.py`. Use the D-pad to move, A to launch/select, and B for menu/back/mute where supported.

## Development Checks

Off-device checks:

```sh
python3 tools/check_project.py
python3 -m pytest
```

Hardware acceptance pass:

1. Copy files to the Pico.
2. Reset and confirm the launcher appears.
3. Launch each current game.
4. Confirm each game can end or return to the menu.
5. Confirm changed pins in `config.py` are honored.

## Original Credits

This project is based on the Raspberry Pi Pico RetroGaming System by YouMakeTech and includes ports or source from Twan37, tyrkelko, Kuba & Stepan, and related Pico game examples.

# Game registry for the launcher and off-device validation.

PLAYABLE_GAMES = [
    {"title": "Pong", "module": "PicoPong", "entrypoint": "pico_pong_main", "category": "Arcade", "status": "ready"},
    {"title": "Snake", "module": "PicoSnake", "entrypoint": "pico_snake_main", "category": "Arcade", "status": "ready"},
    {"title": "Invaders", "module": "PicoInvaders", "entrypoint": "pico_invaders_main", "category": "Arcade", "status": "ready"},
    {"title": "Dino", "module": "PicoDino", "entrypoint": "pico_dino_main", "category": "Runner", "status": "ready"},
    {"title": "2048", "module": "Pico2048", "entrypoint": "pico_2048_main", "category": "Puzzle", "status": "ready"},
    {"title": "Tetris", "module": "PicoTetris", "entrypoint": "pico_tetris_main", "category": "Puzzle", "status": "ready"},
    {"title": "Full Speed", "module": "PicoFullSpeed", "entrypoint": "pico_full_speed_main", "category": "Racing", "status": "ready"},
    {"title": "Lunar Module", "module": "PicoLunarModule", "entrypoint": "pico_lunar_module_main", "category": "Skill", "status": "ready"},
]

PLANNED_GAMES = [
    {"title": "Breakout", "category": "Arcade", "status": "planned-first"},
    {"title": "Minefield", "category": "Puzzle", "status": "planned-first"},
    {"title": "Sokoban", "category": "Puzzle", "status": "planned-first"},
    {"title": "Lights Out", "category": "Puzzle", "status": "planned-first"},
    {"title": "Sliding Puzzle", "category": "Puzzle", "status": "planned-first"},
    {"title": "Flappy Pico", "category": "Arcade", "status": "planned"},
    {"title": "Asteroids Lite", "category": "Arcade", "status": "planned"},
    {"title": "Maze Runner", "category": "Arcade", "status": "planned"},
    {"title": "Frogger Micro", "category": "Arcade", "status": "planned"},
    {"title": "Dodge Rain", "category": "Arcade", "status": "planned"},
    {"title": "Tunnel Racer", "category": "Arcade", "status": "planned"},
    {"title": "Space Duel", "category": "Arcade", "status": "planned"},
    {"title": "Brick Drop", "category": "Arcade", "status": "planned"},
    {"title": "Micro Golf", "category": "Arcade", "status": "planned"},
    {"title": "Jetpack", "category": "Arcade", "status": "planned"},
    {"title": "Memory Match", "category": "Puzzle", "status": "planned"},
    {"title": "Simon", "category": "Puzzle", "status": "planned"},
    {"title": "Yahtzee Lite", "category": "Puzzle", "status": "planned"},
    {"title": "Connect Four", "category": "Strategy", "status": "planned"},
    {"title": "Reversi Mini", "category": "Strategy", "status": "planned"},
    {"title": "Mastermind", "category": "Puzzle", "status": "planned"},
    {"title": "Nonogram Tiny", "category": "Puzzle", "status": "planned"},
    {"title": "Word Guess", "category": "Puzzle", "status": "planned"},
    {"title": "Box Push", "category": "Puzzle", "status": "planned"},
    {"title": "Tower Builder", "category": "Strategy", "status": "planned"},
]

ALL_GAMES = PLAYABLE_GAMES + PLANNED_GAMES

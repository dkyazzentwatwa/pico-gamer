# AGENTS.md

## Project
Pico Gamer is a MicroPython game console for Raspberry Pi Pico-class boards with a 128x64 SSD1306 OLED, six buttons, and an optional buzzer. Keep the project beginner-friendly: files should be easy to copy to a Pico root filesystem and run from `main.py`.

## Hardware Defaults
- Buttons: up GP2, down GP3, left GP4, right GP5, A GP6, B GP7.
- Display: SSD1306 I2C, bus 1, SDA GP14, SCL GP15, address `0x3C`.
- Audio: PWM buzzer on GP18.
- Put hardware changes in `config.py`; do not hard-code pins in games.

## Code Style
- Target MicroPython first. Avoid CPython-only libraries in runtime files.
- Keep game entrypoints named `pico_<game>_main()` unless adding a new engine-native `run(game)` adapter.
- Register playable games in `games.py` with title, module, entrypoint, category, and status.
- Use `PicoGame` or `engine.PicoEngine` helpers for display, input, audio, timing, and menu behavior.
- Keep controls consistent: D-pad moves, A confirms/fires/jumps/rotates, B exits or acts as secondary where useful.

## Checks
Run these from the repo root before handing off:

```sh
python3 tools/check_project.py
python3 -m pytest
```

`tools/check_project.py` avoids MicroPython imports and validates syntax plus the game registry. Hardware verification still requires copying files to the Pico and launching each game.

## Adding Games
Start with a single `PicoName.py` file, expose one entrypoint, add it to `PLAYABLE_GAMES`, and keep sprites/data small enough for Pico memory. Prefer games that fit the 128x64 screen without scrolling instructions.

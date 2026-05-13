# Registry-driven launcher for Pico Gamer.

import time

from engine import PicoEngine, load_entrypoint
from games import PLAYABLE_GAMES


def show_launch_error(game, err):
    display = game.display
    game.sound(0)
    game.clear()
    display.text("LOAD ERROR", 24, 8, 1)
    display.text(str(err)[:16], 0, 24, 1)
    display.text("B: MENU", 36, 52, 1)
    game.show()
    game.wait_release()
    while not game.pressed("b"):
        time.sleep_ms(20)
    game.wait_release()


def run_selected(game, item):
    game.clear()
    game.center_text(item["title"], 18)
    game.center_text("LOADING...", 42)
    game.show()
    try:
        entrypoint = load_entrypoint(item["module"], item["entrypoint"])
        game.sound(0)
        entrypoint()
    except Exception as err:
        show_launch_error(game, err)
    finally:
        game.sound(0)
        game.wait_release()


def main():
    game = PicoEngine()
    current = 0
    game.draw_menu(PLAYABLE_GAMES, current)
    game.wait_release()

    while True:
        if game.pressed("down") or game.pressed("right"):
            current = (current + 1) % len(PLAYABLE_GAMES)
            game.beep(900, 35)
            game.draw_menu(PLAYABLE_GAMES, current)
            game.wait_release()
        elif game.pressed("up") or game.pressed("left"):
            current = (current - 1) % len(PLAYABLE_GAMES)
            game.beep(700, 35)
            game.draw_menu(PLAYABLE_GAMES, current)
            game.wait_release()
        elif game.pressed("a"):
            game.beep()
            game.wait_release()
            run_selected(game, PLAYABLE_GAMES[current])
            game.draw_menu(PLAYABLE_GAMES, current)
        elif game.pressed("b"):
            game.toggle_mute()
            game.beep(300, 35)
            game.draw_menu(PLAYABLE_GAMES, current)
            game.wait_release()
        else:
            time.sleep_ms(20)


if __name__ == "__main__":
    main()

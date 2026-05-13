# Game "Lunar Module" by Kuba & Stepan

from PicoGame import PicoGame
import time


def pico_lunar_module_main():
    game = PicoGame()
    if not start_screen(game):
        return

    level = 1
    x = 8
    y = 2
    vx = 1
    vy = 0
    fuel = 30

    while True:
        if game.button_B():
            game.sound(0)
            game.wait_release()
            return

        thrust = False
        if (game.button_A() or game.button_up()) and fuel > 0:
            thrust = True
            vy -= 2
            fuel -= 1
            game.sound(900)
        else:
            game.sound(0)

        if game.button_left() and fuel > 0:
            vx -= 1
            fuel = max(0, fuel - 1)
        if game.button_right() and fuel > 0:
            vx += 1
            fuel = max(0, fuel - 1)

        vy += 1
        x += vx
        y += int(vy / 2)

        if x < 0:
            x = 0
            vx = 1
        if x > 120:
            x = 120
            vx = -1

        game.fill(0)
        game.text("F:" + str(fuel), 0, 0, 1)
        game.top_right_corner_text("V:" + str(vy))
        game.rect(94, 62, 22, 2, 1)
        draw_lander(game, x, y, thrust)
        game.show()

        if y >= 52:
            landed = x >= 92 and x <= 112 and abs(vx) <= 3 and vy <= 6 and fuel >= 0
            game.sound(0)
            if landed:
                game.fill(0)
                game.center_text("LANDING OK", 18)
                game.center_text("LEVEL " + str(level + 1), 36)
                game.show()
                time.sleep_ms(1200)
                level += 1
                x = 8
                y = 2
                vx = level
                vy = 0
                fuel = max(18, 32 - level)
            else:
                game.sound(160)
                time.sleep_ms(300)
                game.sound(0)
                if not end_screen(game, level):
                    return
                level = 1
                x = 8
                y = 2
                vx = 1
                vy = 0
                fuel = 30

        if fuel <= 0 and y < 52:
            fuel = 0

        time.sleep_ms(90)


def draw_lander(game, x, y, thrust):
    game.rect(int(x) + 2, int(y) + 2, 6, 5, 1)
    game.rect(int(x) + 3, int(y), 4, 3, 1)
    game.vline(int(x) + 1, int(y) + 5, 5, 1)
    game.vline(int(x) + 8, int(y) + 5, 5, 1)
    if thrust:
        game.vline(int(x) + 5, int(y) + 8, 7, 1)


def start_screen(game):
    game.fill(0)
    game.center_text("LUNAR MODULE", 14)
    game.text("A/up thrust", 20, 36, 1)
    game.text("A start B menu", 8, 52, 1)
    game.show()
    game.wait_release()
    while True:
        if game.button_A():
            game.wait_release()
            return True
        if game.button_B():
            game.wait_release()
            return False
        time.sleep_ms(20)


def end_screen(game, level):
    game.fill(0)
    game.center_text("CRASH")
    game.text("Level " + str(level), 36, 36, 1)
    game.text("A again B menu", 8, 52, 1)
    game.show()
    game.wait_release()
    while True:
        if game.button_A():
            game.wait_release()
            return True
        if game.button_B():
            game.wait_release()
            return False
        time.sleep_ms(20)


if __name__ == "__main__":
    pico_lunar_module_main()

# Game "Full Speed" by Kuba & Stepan

from PicoGame import PicoGame
import time
import random


def pico_full_speed_main():
    game = PicoGame()

    if not start_screen(game):
        return

    player_x = 0
    road_shift = 0
    road_dir = 1
    obstacle_y = -20
    obstacle_x = 0
    speed = 1
    score = 0

    while True:
        if game.button_B():
            game.sound(0)
            game.wait_release()
            return
        if game.button_left():
            player_x -= 3
        if game.button_right():
            player_x += 3

        road_shift += road_dir
        if road_shift <= -28 or road_shift >= 24:
            road_dir = -road_dir

        obstacle_y += speed + 1
        if obstacle_y > 64:
            obstacle_y = -10
            obstacle_x = random.randint(-34, 34)
            score += 1
            if score % 8 == 0 and speed < 5:
                speed += 1

        road_center = road_shift
        if road_shift < -12:
            player_x += 1
        elif road_shift > 12:
            player_x -= 1

        crash = player_x < -46 or player_x > 46
        if obstacle_y > 42 and obstacle_y < 62:
            if abs(player_x - obstacle_x - road_center // 2) < 7:
                crash = True

        game.fill(0)
        game.text("S:" + str(score), 0, 0, 1)
        game.top_right_corner_text(str((score + 1) * 5) + "k")
        draw_road(game, road_shift)
        draw_bike(game, 64 + player_x, 56, 0)
        if obstacle_y > -8:
            draw_bike(game, 64 + obstacle_x + road_center // 2, obstacle_y, 0)
        game.show()

        if crash:
            game.sound(180)
            time.sleep_ms(350)
            game.sound(0)
            if not end_screen(game, score):
                return
            player_x = 0
            road_shift = 0
            road_dir = 1
            obstacle_y = -20
            obstacle_x = 0
            speed = 1
            score = 0

        time.sleep_ms(70)


def draw_road(game, shift):
    game.line(18 + shift // 4, 34, 110 + shift // 4, 34, 1)
    game.line(46 + shift, 34, 16, 63, 1)
    game.line(82 + shift, 34, 112, 63, 1)
    game.line(62 + shift // 2, 38, 60, 63, 1)
    game.line(66 + shift // 2, 38, 68, 63, 1)


def draw_bike(game, x, y, tilt):
    game.rect(int(x) - 2 + tilt, int(y) - 6, 4, 3, 1)
    game.rect(int(x) - 1, int(y) - 2, 2, 4, 1)
    game.pixel(int(x), int(y) - 8, 1)


def start_screen(game):
    game.fill(0)
    game.center_text("FULL SPEED", 14)
    game.text("Left/right steer", 0, 36, 1)
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


def end_screen(game, score):
    game.fill(0)
    game.center_text("CRASH")
    game.text("Score " + str(score), 32, 36, 1)
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
    pico_full_speed_main()

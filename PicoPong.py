# PicoPong.py: a simple Pong game by Vincent Mistler (YouMakeTech)

from PicoGame import PicoGame
import time
import random


def pico_pong_main():
    game = PicoGame()

    ball_size = 4
    paddle_width = 18
    paddle_height = 4
    paddle_y = game.SCREEN_HEIGHT - 10
    paddle_speed = 4

    while True:
        ball_x = 64
        ball_y = 16
        ball_vx = random.choice([-2, 2])
        ball_vy = 2
        paddle_x = int((game.SCREEN_WIDTH - paddle_width) / 2)
        score = 0
        tick = 0

        game.fill(0)
        game.center_text("PONG", 1)
        game.text("A start  B menu", 4, 46, 1)
        game.show()
        game.wait_release()
        while not game.button_A() and not game.button_B():
            time.sleep_ms(20)
        if game.button_B():
            game.wait_release()
            return
        game.wait_release()

        while True:
            if game.button_B():
                game.sound(0)
                game.wait_release()
                return
            if game.button_left():
                paddle_x -= paddle_speed
            if game.button_right():
                paddle_x += paddle_speed
            if paddle_x < 0:
                paddle_x = 0
            if paddle_x + paddle_width > game.SCREEN_WIDTH:
                paddle_x = game.SCREEN_WIDTH - paddle_width

            ball_x += ball_vx
            ball_y += ball_vy

            collision = False
            if ball_x <= 0:
                ball_x = 0
                ball_vx = -ball_vx
                collision = True
            if ball_x + ball_size >= game.SCREEN_WIDTH:
                ball_x = game.SCREEN_WIDTH - ball_size
                ball_vx = -ball_vx
                collision = True
            if ball_y <= 0:
                ball_y = 0
                ball_vy = -ball_vy
                collision = True
            if ball_y + ball_size >= paddle_y:
                if ball_x + ball_size >= paddle_x and ball_x <= paddle_x + paddle_width:
                    ball_y = paddle_y - ball_size
                    ball_vy = -abs(ball_vy)
                    offset = ball_x - (paddle_x + int(paddle_width / 2))
                    ball_vx = max(-4, min(4, ball_vx + int(offset / 8)))
                    if ball_vx == 0:
                        ball_vx = random.choice([-1, 1])
                    score += 10
                    collision = True

            if ball_y + ball_size > game.SCREEN_HEIGHT:
                game.sound(200)
                time.sleep_ms(250)
                game.sound(0)
                if not game_over(game, score):
                    return
                break

            if collision:
                game.sound(700 if tick % 2 else 500)
            else:
                game.sound(0)

            game.fill(0)
            game.fill_rect(paddle_x, paddle_y, paddle_width, paddle_height, 1)
            game.fill_rect(int(ball_x), int(ball_y), ball_size, ball_size, 1)
            game.top_right_corner_text(str(score))
            game.show()
            tick += 1
            time.sleep_ms(24)


def game_over(game, score):
    game.fill(0)
    game.center_text("GAME OVER")
    game.top_right_corner_text(str(score))
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
    pico_pong_main()

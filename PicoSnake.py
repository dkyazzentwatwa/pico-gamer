# Original source code from https://github.com/Twan37/PicoSnake

from PicoGame import PicoGame
import time
import random


CELL = 8
GRID_W = 16
GRID_H = 8
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3


def pico_snake_main():
    game = PicoGame()

    while True:
        if not start_screen(game):
            return

        snake = [[GRID_W // 2, GRID_H // 2]]
        direction = random.choice([UP, DOWN, LEFT, RIGHT])
        pending = direction
        food = place_food(snake)
        score = 0
        delay = 170
        alive = True

        while alive:
            if game.button_B():
                game.sound(0)
                game.wait_release()
                return
            if game.button_up() and direction != DOWN:
                pending = UP
            elif game.button_down() and direction != UP:
                pending = DOWN
            elif game.button_left() and direction != RIGHT:
                pending = LEFT
            elif game.button_right() and direction != LEFT:
                pending = RIGHT

            direction = pending
            head = [snake[-1][0], snake[-1][1]]
            if direction == UP:
                head[1] -= 1
            elif direction == DOWN:
                head[1] += 1
            elif direction == LEFT:
                head[0] -= 1
            else:
                head[0] += 1

            if head[0] < 0 or head[0] >= GRID_W or head[1] < 0 or head[1] >= GRID_H or head in snake:
                alive = False
                break

            snake.append(head)
            if head == food:
                score += 1
                game.sound(900)
                food = place_food(snake)
                delay = max(80, delay - 5)
            else:
                game.sound(0)
                snake.pop(0)

            draw(game, snake, food, score)
            time.sleep_ms(delay)

        game.sound(180)
        time.sleep_ms(300)
        game.sound(0)
        if not end_screen(game, score):
            return


def place_food(snake):
    choices = []
    for x in range(GRID_W):
        for y in range(GRID_H):
            if [x, y] not in snake:
                choices.append([x, y])
    if not choices:
        return [0, 0]
    return random.choice(choices)


def draw(game, snake, food, score):
    game.fill(0)
    game.top_right_corner_text(str(score))
    game.fill_rect(food[0] * CELL + 2, food[1] * CELL + 2, 4, 4, 1)
    for segment in snake:
        game.rect(segment[0] * CELL, segment[1] * CELL, CELL, CELL, 1)
    game.show()


def start_screen(game):
    game.fill(0)
    game.center_text("SNAKE", 14)
    game.text("D-pad turn", 24, 36, 1)
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
    game.center_text("GAME OVER", 16)
    game.text("Length " + str(score + 1), 28, 36, 1)
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
    pico_snake_main()

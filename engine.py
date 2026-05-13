from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
import time

import config


class PicoEngine:
    def __init__(self):
        self.width = config.SCREEN_WIDTH
        self.height = config.SCREEN_HEIGHT
        self.buttons = {}
        for name, pin in config.BUTTON_PINS.items():
            self.buttons[name] = Pin(pin, Pin.IN, Pin.PULL_UP)
        self.buzzer = PWM(Pin(config.BUZZER_PIN))
        self.i2c = I2C(
            config.I2C_ID,
            sda=Pin(config.I2C_SDA_PIN),
            scl=Pin(config.I2C_SCL_PIN),
            freq=config.I2C_FREQ,
        )
        self.display = SSD1306_I2C(
            config.SCREEN_WIDTH,
            config.SCREEN_HEIGHT,
            self.i2c,
            addr=config.I2C_ADDR,
        )
        self.muted = False

    def pressed(self, name):
        return self.buttons[name].value() == 0

    def any_button(self):
        for button in self.buttons.values():
            if button.value() == 0:
                return True
        return False

    def wait_release(self):
        while self.any_button():
            time.sleep_ms(20)

    def wait_press(self):
        while not self.any_button():
            time.sleep_ms(20)

    def sleep_ms(self, ms):
        time.sleep_ms(ms)

    def clear(self):
        self.display.fill(0)

    def show(self):
        self.display.show()

    def center_text(self, text, y=None, color=1):
        if y is None:
            y = int(self.height / 2) - 4
        x = int(self.width / 2) - int(len(text) * 4)
        if x < 0:
            x = 0
        self.display.text(text, x, y, color)

    def right_text(self, text, y=0, color=1):
        x = self.width - len(text) * 8
        if x < 0:
            x = 0
        self.display.text(text, x, y, color)

    def beep(self, freq=1000, ms=60):
        self.sound(freq)
        time.sleep_ms(ms)
        self.sound(0)

    def sound(self, freq, duty_u16=2000):
        if self.muted or freq <= 0:
            self.buzzer.duty_u16(0)
            return
        self.buzzer.freq(freq)
        self.buzzer.duty_u16(duty_u16)

    def toggle_mute(self):
        self.muted = not self.muted
        self.sound(0)
        return self.muted

    def title_screen(self, title, subtitle="A START  B BACK"):
        self.clear()
        self.display.rect(0, 0, self.width, self.height, 1)
        self.center_text(title, 20)
        self.center_text(subtitle, 42)
        self.show()
        self.wait_release()
        while True:
            if self.pressed("a"):
                self.beep()
                self.wait_release()
                return True
            if self.pressed("b"):
                self.beep(300)
                self.wait_release()
                return False
            time.sleep_ms(20)

    def game_over(self, title, detail="A AGAIN  B MENU"):
        self.sound(0)
        self.clear()
        self.display.fill_rect(0, 18, self.width, 28, 1)
        self.center_text(title, 24, 0)
        self.center_text(detail, 52)
        self.show()
        self.wait_release()
        while True:
            if self.pressed("a"):
                self.beep()
                self.wait_release()
                return True
            if self.pressed("b"):
                self.beep(300)
                self.wait_release()
                return False
            time.sleep_ms(20)

    def draw_menu(self, items, current):
        total = len(items)
        rows = config.MENU_ROWS
        first = current - rows + 1 if current >= rows else 0
        if first + rows > total:
            first = max(0, total - rows)
        self.clear()
        self.display.text("PICO GAMER", 0, 0, 1)
        self.right_text(str(current + 1) + "/" + str(total), 0)
        for row in range(rows):
            index = first + row
            if index >= total:
                break
            y = 10 + row * 8
            title = items[index]["title"]
            if index == current:
                self.display.fill_rect(0, y, self.width, 8, 1)
                self.display.text(title[:16], 2, y, 0)
            else:
                self.display.text(title[:16], 2, y, 1)
        current_game = items[current]
        footer = current_game["category"][:9] + " " + current_game["status"][:6]
        self.display.fill_rect(0, 58, self.width, 6, 0)
        self.display.text(footer[:16], 0, 56, 1)
        self.show()


def load_entrypoint(module_name, entrypoint):
    module = __import__(module_name)
    return getattr(module, entrypoint)

# Hardware defaults for the original Raspberry Pi Pico RetroGaming System.

SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

BUTTON_PINS = {
    "up": 2,
    "down": 3,
    "left": 4,
    "right": 5,
    "a": 6,
    "b": 7,
}

BUZZER_PIN = 18

I2C_ID = 1
I2C_SDA_PIN = 14
I2C_SCL_PIN = 15
I2C_FREQ = 400000
I2C_ADDR = 0x3C

MENU_ROWS = 6
FRAME_DELAY_MS = 33

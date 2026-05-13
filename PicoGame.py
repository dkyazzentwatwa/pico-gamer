# PicoGame.py by YouMakeTech
# A class to easily write games for the Raspberry Pi Pico RetroGaming System
from machine import Pin, PWM, I2C
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB
import time

import config

class PicoGame(SSD1306_I2C):
    def __init__(self):
        self.SCREEN_WIDTH = config.SCREEN_WIDTH
        self.SCREEN_HEIGHT = config.SCREEN_HEIGHT
        self.__up = Pin(config.BUTTON_PINS["up"], Pin.IN, Pin.PULL_UP)
        self.__down = Pin(config.BUTTON_PINS["down"], Pin.IN, Pin.PULL_UP)
        self.__left = Pin(config.BUTTON_PINS["left"], Pin.IN, Pin.PULL_UP)
        self.__right = Pin(config.BUTTON_PINS["right"], Pin.IN, Pin.PULL_UP)
        self.__button_A = Pin(config.BUTTON_PINS["a"], Pin.IN, Pin.PULL_UP)
        self.__button_B = Pin(config.BUTTON_PINS["b"], Pin.IN, Pin.PULL_UP)
        self.__buzzer = PWM(Pin(config.BUZZER_PIN))
        
        self.__i2c = I2C(
            config.I2C_ID,
            sda=Pin(config.I2C_SDA_PIN),
            scl=Pin(config.I2C_SCL_PIN),
            freq=config.I2C_FREQ,
        )
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.__i2c, addr=config.I2C_ADDR)
        
        self.__fb=[] # Array of FrameBuffer objects for sprites
        self.__w=[]
        self.__h=[]
        
        self.__mute = False
    
    def center_text(self, s, color = 1, y = None):
        if color not in (0, 1) and y is None:
            y = color
            color = 1
        x = int(self.width/2)- int(len(s)/2 * 8)
        if x < 0:
            x = 0
        if y is None:
            y = int(self.height/2) - 8
        self.text(s, x, y, color)
        
    def top_right_corner_text(self, s, color = 1):
        x = self.width - int(len(s) * 8)
        if x < 0:
            x = 0
        y = 0
        self.text(s, x, y, color)
        
    def add_sprite(self, buffer, w, h):
        fb = FrameBuffer(buffer, w, h, MONO_HLSB)
        self.__fb.append(fb)
        self.__w.append(w)
        self.__h.append(h)
        return len(self.__fb) - 1
       
    def sprite(self, n, x, y, key = 0):
        self.blit(self.__fb[n], x, y, key)
        
    def sprite_width(self,n):
        return self.__w[n]
    
    def sprite_height(self,n):
        return self.__h[n]
    
    def sprites_intersection(self, x1, y1, w1, h1, x2, y2, w2, h2):
    # return true if the 2 sprites rectangles
    # (x1,y1,w1,h1) and (x2,y2,w2,h2) overlaps
        overlap = True
        if x2 > x1 + w1 - 1:
            overlap = False
        if x2 + w2 - 1 < x1:
            overlap = False
        if y2 > y1 + h1 -1:
            overlap = False
        if y2 + h2 -1 < y1:
            overlap = False
        return overlap
    
    def sprites_collision(self, n, x1, y1, m, x2, y2):
        if self.sprites_intersection(x1, y1, self.sprite_width(n), self.sprite_height(n), x2, y2, self.sprite_width(m), self.sprite_height(m)):
            dx = max(x1, x2)
            dy = max(y1, y2)
            dw = min(x1 + self.sprite_width(n), x2 + self.sprite_width(m)) - dx
            dh = min(y1 + self.sprite_height(n), y2 + self.sprite_height(m)) - dy
            for j in range(dy, dy + dh):
                for i in range(dx, dx + dw):
                    if self.__fb[n].pixel(i - x1, j - y1) and self.__fb[m].pixel(i - x2, j - y2):
                        return True          
        return False
            
    def button_up(self):
        return self.__up.value()==0
    
    def button_down(self):
        return self.__down.value()==0
    
    def button_left(self):
        return self.__left.value()==0
    
    def button_right(self):
        return self.__right.value()==0
    
    def button_A(self):
        return self.__button_A.value()==0
    
    def button_B(self):
        return self.__button_B.value()==0
    
    def any_button(self):
        # returns True if any button is pressed
        button_pressed=False
        if self.button_up():
            button_pressed = True
        if self.button_down():
            button_pressed = True
        if self.button_left():
            button_pressed = True
        if self.button_right():
            button_pressed = True
        if self.button_A():
            button_pressed = True
        if self.button_B():
            button_pressed = True
        return button_pressed

    def wait_release(self):
        while self.any_button():
            time.sleep_ms(20)

    def wait_press(self):
        while not self.any_button():
            time.sleep_ms(20)

    def toggle_mute(self):
        self.__mute = not self.__mute
        self.sound(0)
        return self.__mute

    def is_muted(self):
        return self.__mute

    def should_exit(self):
        return self.button_B()
    
    def sound(self, freq, duty_u16 = 2000):
        if self.__mute or freq <= 0:
            self.__buzzer.duty_u16(0)
            return
        # Make a sound at the selected frequency in Hz
        self.__buzzer.freq(freq)
        self.__buzzer.duty_u16(duty_u16)
       

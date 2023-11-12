from pico2d import *

import game_framework
import math

PIXEL_PER_METER = (10.0 / 0.3)
TURN_SPEED_KMPH = 10.0
TURN_SPEED_MPM = (TURN_SPEED_KMPH * 1000.0 / 60.0)
TURN_SPEED_MPS = (TURN_SPEED_MPM / 60.0)
TURN_SPEED_PPS = (TURN_SPEED_MPS * PIXEL_PER_METER)

class Arrow():
    img = None
    def __init__(self, x = 580, y = 50):
        self.x = x
        self.y = y
        self.degree = 0
        self.tunning = 1
        if Arrow.img == None:
            Arrow.img = load_image('../resource/arrow.png')

    def draw(self):
        Arrow.img.clip_composite_draw(0, 0, 300, 300, math.radians(self.degree), 'w', self.x, self.y, 90, 80)

    def update(self):
        self.degree += self.tunning * TURN_SPEED_PPS * game_framework.frame_time

        self.x = 450 + (580 - 450) * math.cos(math.radians(self.degree))
        self.y = 50 + (580 - 450) * math.sin(math.radians(self.degree))

        if self.degree >= 180:
            self.tunning = -1
        elif self.degree <= 0:
            self.tunning = 1
        pass
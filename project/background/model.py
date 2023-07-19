'''The background in a shooter game in the vein of Space Invaders'''

from random import random
import pyxel
from data.logger import get_logger

_log = get_logger(__name__)
STAR_COUNT = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5

class Background:
    '''Setting up the game environment'''
    def __init__(self):
        self.star_list = []
        for i in range(STAR_COUNT):
            self.star_list.append(
                (random() * pyxel.width,random() *
                 pyxel.height,random() * 1.5 + 1)
            )

    def update(self):
        '''Updates the background'''
        for i, (x, y, speed) in enumerate(self.star_list):
            y += speed
            if y >= pyxel.height:
                y -= pyxel.height
            self.star_list[i] = (x, y, speed)

    def draw(self):
        '''Draws the new background'''
        for (x, y, speed) in self.star_list:
            pyxel.pset(x, y, STAR_COLOR_HIGH if speed > 1.8 else STAR_COLOR_LOW)
'''An enemy in a Space Invaders type game'''

from random import random
import pyxel
from data.logger import get_logger

_log = get_logger(__name__)
ENEMY_WIDTH = 8
ENEMY_HEIGHT = 8
ENEMY_SPEED = 1.5

class Enemy:
    '''Enemy to be stopped'''
    enemy_list = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)
        self.enemy_list.append(self)

    def update(self):
        '''Updates the position of the enemy'''
        if (pyxel.frame_count + self.offset) % 60 < 30:
            self.x += ENEMY_SPEED
            self.dir = 1
        else:
            self.x -= ENEMY_SPEED
            self.dir = -1

        self.y += ENEMY_SPEED

        if self.y > pyxel.height - 1:
            self.alive = False

    def draw(self):
        '''Draws the enemy in the new position'''
        _log.info("In enemy draw")
        pyxel.blt(self.x, self.y, 0, 8, 0, self.w * self.dir, self.h, 0)

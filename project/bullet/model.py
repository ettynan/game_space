'''A blast in a shooter game in the vein of Space Invaders'''

import pyxel
from data.logger import get_logger

_log = get_logger(__name__)
BULLET_COLOR = 11
BULLET_SPEED = 4
BULLET_WIDTH=2
BULLET_HEIGHT=8

class Bullet:
    '''Bullet to shoot the invaders'''
    bullet_list = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.alive = True
        self.bullet_list.append(self)

    def update(self):
        '''Updates the bullet position'''
        self.y -= BULLET_SPEED

        if self.y + self.h - 1 < 0:
            self.alive = False

    def draw(self):
        '''Draws the bullet in the updated position'''
        _log.info("In bullet draw")
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)
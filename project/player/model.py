'''A player in a shooter game in the vein of Space Invaders'''

import pyxel
from data.logger import get_logger
from bullet.model import Bullet, BULLET_HEIGHT, BULLET_WIDTH

_log = get_logger(__name__)
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2

class Player:
    '''Player for the game'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = PLAYER_WIDTH
        self.h = PLAYER_HEIGHT
        self.alive = True

    def update(self):
        '''Updates the player position based on direction'''
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= PLAYER_SPEED
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += PLAYER_SPEED
        self.x = max(self.x, 0)
        self.x = min(self.x, pyxel.width - self.w)
        self.y = max(self.y, 0)
        self.y = min(self.y, pyxel.height - self.h)

        if pyxel.btnp(pyxel.KEY_SPACE):
            Bullet(self.x + (PLAYER_WIDTH - BULLET_WIDTH)/ 2,
                   self.y - BULLET_HEIGHT/2)

            pyxel.play(0, 0)

    def draw(self):
        '''Draws the updated player'''
        _log.info("In player draw")
        pyxel.blt(self.x, self.y, 0, 0, 0, self.w, self.h, 0)
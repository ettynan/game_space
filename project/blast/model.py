'''A blast in a Space Invaders type game'''

import pyxel
from data.logger import get_logger

_log = get_logger(__name__)
BLAST_START_RADIUS = 1
BLAST_END_RADIUS = 8

class Blast:
    '''Destructive blast'''
    blast_list = []

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BLAST_START_RADIUS
        self.alive = True
        self.blast_list.append(self)
        self.BLAST_COLOR_IN = 7
        self.BLAST_COLOR_OUT = 10

    def update(self):
        '''Updates the position of the blast'''
        self.radius += 1

        if self.radius > BLAST_END_RADIUS:
            self.alive = False

    def draw(self):
        '''Draws the blast in the updated position'''
        _log.info("In Blast draw")
        pyxel.circ(self.x, self.y, self.radius, self.BLAST_COLOR_IN)
        pyxel.circb(self.x, self.y, self.radius, self.BLAST_COLOR_OUT)

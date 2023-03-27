'''A shooter game in the vein of Space Invaders'''

from random import random
import pyxel

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
STAR_COUNT = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2
BULLET_WIDTH = 8
BULLET_HEIGHT = 8
BULLET_SPEED = 4
ENEMY_WIDTH = 8
ENEMY_HEIGHT = 8
ENEMY_SPEED = 1.5
BLAST_START_RADIUS = 1
BLAST_END_RADIUS = 1
BLAST_COLOR_IN = 7
BLAST_COLOR_OUT = 10
enemy_list = []
bullet_list = []
blast_list = []


def update_list(list):
    '''Takes in a list and updates it'''
    for elem in list:
        elem.update()

def draw_list(list):
    '''Takes in a list and draws it'''
    for elem in list:
        elem.draw()

def cleanup_list(list):
    '''Takes in a list, loops through it and removes old items'''
    i = 0
    while i<len(list):
        elem = list[i]
        if not elem.alive:
            list.pop(i)
        else:
            i += 1


class Background:
    def __init__(self):
        self.star_list = []
        for i in range(STAR_COUNT):
            self.star_list.append(
                (random() * pyxel.width,random() * pyxel.height,random() * 1.5 + 1)
            )


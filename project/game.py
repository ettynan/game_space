'''A shooter game in the vein of Space Invaders'''

from random import random
import pyxel
from data.logger import get_logger
from blast.model import Blast
from bullet.model import Bullet
from enemy.model import Enemy, ENEMY_WIDTH, ENEMY_HEIGHT
from background.model import Background
from player.model import Player, PLAYER_WIDTH, PLAYER_HEIGHT

_log = get_logger(__name__)

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2

# User interface
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

class App:
    '''Game window and game play'''
    def __init__(self):
        pyxel.init(120, 160, title="All your base are belong to us!")
        pyxel.image(0).set(
            0,
            0,
            ["00c00c00",
             "0c7007c0",
             "0c7007c0",
             "c703b07c",
             "77033077",
             "785cc587",
             "85c77c58",
             "0c0880c0"
             ])
        pyxel.image(0).set(
            8,
            0,
            ["00088000",
             "00ee1200",
             "08e2b180",
             "02882820",
             "00222200",
             "00012280",
             "08208008",
             "80008000"
             ])
        pyxel.sound(0).set("a3a2c1a1", "p", "7", "s", 5)
        pyxel.sound(1).set("a3a2c2c2", "n", "7742", "s", 10)
        self.scene = SCENE_TITLE
        self.score = 0
        self.background = Background()
        self.player = Player(pyxel.width/2, pyxel.height - 20)
        pyxel.run(self.update, self.draw)

    def update(self):
        '''Update the background based on circumstance'''
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.background.update()

        if self.scene == SCENE_TITLE:
            self.update_title_scene()
        elif self.scene == SCENE_PLAY:
            self.update_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover_scene()

    def update_title_scene(self):
        '''Updates the title scene based on play'''
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY

    def update_play_scene(self):
        '''Updates the main play content'''
        if pyxel.frame_count % 6 == 0:
            Enemy(random() * (pyxel.width - PLAYER_WIDTH), 0)
        for e in Enemy.enemy_list:
            for b in Bullet.bullet_list:
                # Determine if enemy hit by bullet
                if (e.x + e.w > b.x
                    and b.x + b.w > e.x
                    and e.y + e.h > b.y
                    and b.y + b.h > e.y):
                    e.alive = False
                    b.alive = False
                    Blast.blast_list.append(Blast(e.x + ENEMY_WIDTH/2,
                                            e.y + ENEMY_HEIGHT/2))
                    pyxel.play(1, 1)
                    self.score += 10
        for enemy in Enemy.enemy_list:
            # Determine if player hit by enemy itself
            if(self.player.x + self.player.w > enemy.x
               and enemy.x + enemy.w > self.player.x
               and self.player.y + self.player.h > enemy.y
               and enemy.y + enemy.h > self.player.y):
                enemy.alive = False
                Blast.blast_list.append(Blast(self.player.x + PLAYER_WIDTH/2,
                                        self.player.y + PLAYER_HEIGHT/2))
                pyxel.play(1, 1)
                self.scene = SCENE_GAMEOVER
            self.player.update()
            update_list(Bullet.bullet_list)
            update_list(Enemy.enemy_list)
            update_list(Blast.blast_list)
            cleanup_list(Enemy.enemy_list)
            cleanup_list(Bullet.bullet_list)
            cleanup_list(Blast.blast_list)

    def update_gameover_scene(self):
        '''Update game over scene'''
        update_list(Bullet.bullet_list)
        update_list(Enemy.enemy_list)
        update_list(Blast.blast_list)
        cleanup_list(Enemy.enemy_list)
        cleanup_list(Bullet.bullet_list)
        cleanup_list(Blast.blast_list)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width/2
            self.player.y = pyxel.height - 20
            self.score = 0
            Enemy.enemy_list.clear()
            Bullet.bullet_list.clear()
            Blast.blast_list.clear()

    def draw(self):
        '''Draw the scene based on circumstance'''
        pyxel.cls(0)
        self.background.draw()

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_PLAY:
            self.draw_play_scene()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover_scene()

        pyxel.text(39, 4, "SCORE{:5}".format(self.score), 7)

    def draw_title_scene(self):
        '''Draw the initial title scene'''
        _log.info("In draw title scene")
        pyxel.text(35, 66, "Start Game", pyxel.frame_count %16)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        '''Prepare effects for game play'''
        _log.info("Draw play scene")
        self.player.draw()
        draw_list(Bullet.bullet_list)
        draw_list(Enemy.enemy_list)
        draw_list(Blast.blast_list)

    def draw_gameover_scene(self):
        '''Prepare effects for gameover scene'''
        draw_list(Bullet.bullet_list)
        draw_list(Enemy.enemy_list)
        draw_list(Blast.blast_list)
        pyxel.text(43, 66, "GAMEOVER", 8)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)


App()
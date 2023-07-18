'''A shooter game in the vein of Space Invaders'''

from random import random
import pyxel
from data.logger import get_logger

# User interface
_log = get_logger(__name__)

SCENE_TITLE = 0
SCENE_PLAY = 1
SCENE_GAMEOVER = 2
STAR_COUNT = 100
STAR_COLOR_HIGH = 12
STAR_COLOR_LOW = 5
PLAYER_WIDTH = 8
PLAYER_HEIGHT = 8
PLAYER_SPEED = 2
BULLET_WIDTH = 2
BULLET_HEIGHT = 8
BULLET_COLOR = 11
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

class Bullet:
    '''Bullet to shoot the invaders'''
    _log.info("In bullet")
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = BULLET_WIDTH
        self.h = BULLET_HEIGHT
        self.alive = True

        bullet_list.append(self)

    def update(self):
        '''Updates the bullet position'''
        self.y -= BULLET_SPEED

        if self.y + self.h - 1 < 0:
            self.alive = False

    def draw(self):
        '''Draws the bullet in the updated position'''
        _log.info("In bullet draw")
        pyxel.rect(self.x, self.y, self.w, self.h, BULLET_COLOR)

class Enemy:
    '''Enemy to be stopped'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = ENEMY_WIDTH
        self.h = ENEMY_HEIGHT
        self.dir = 1
        self.alive = True
        self.offset = int(random() * 60)

        enemy_list.append(self)

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

class Blast:
    '''Destructive blast'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BLAST_START_RADIUS
        self.alive = True

        blast_list.append(self)

    def update(self):
        '''Updates the position of the blast'''
        self.radius += 1

        if self.radius > BLAST_END_RADIUS:
            self.alive = False

    def draw(self):
        '''Draws the blast in the updated position'''
        _log.info("In Blast draw")
        pyxel.circ(self.x, self.y, self.radius, BLAST_COLOR_IN)
        pyxel.circb(self.x, self.y, self.radius,BLAST_COLOR_OUT)

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
        for e in enemy_list:
            for b in bullet_list:
                # Determine if enemy hit by bullet
                if (e.x + e.w > b.x
                    and b.x + b.w > e.x
                    and e.y + e.h > b.y
                    and b.y + b.h > e.y):
                    e.alive = False
                    b.alive = False
                    blast_list.append(Blast(e.x + ENEMY_WIDTH/2,
                                            e.y + ENEMY_HEIGHT/2))
                    pyxel.play(1, 1)
                    self.score += 10
        for enemy in enemy_list:
            # Determine if player hit by enemy itself
            if(self.player.x + self.player.w > enemy.x
               and enemy.x + enemy.w > self.player.x
               and self.player.y + self.player.h > enemy.y
               and enemy.y + enemy.h > self.player.y):
                blast_list.append(Blast(self.player.x + PLAYER_WIDTH/2,
                                        self.player.y + PLAYER_HEIGHT/2))
                pyxel.play(1, 1)
                self.scene = SCENE_GAMEOVER
            self.player.update()
            update_list(bullet_list)
            update_list(enemy_list)
            update_list(blast_list)
            cleanup_list(enemy_list)
            cleanup_list(bullet_list)
            cleanup_list(blast_list)

    def update_gameover_scene(self):
        '''Update game over scene'''
        update_list(bullet_list)
        update_list(enemy_list)
        update_list(blast_list)
        cleanup_list(enemy_list)
        cleanup_list(bullet_list)
        cleanup_list(blast_list)
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.scene = SCENE_PLAY
            self.player.x = pyxel.width/2
            self.player.y = pyxel.height - 20
            self.score = 0
            enemy_list.clear()
            bullet_list.clear()
            blast_list.clear()

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
        pyxel.text(35, 66, "Start Game", pyxel.frame_count %16)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)

    def draw_play_scene(self):
        '''Prepare effects for game play'''
        _log.info("Draw play scene")
        self.player.draw()
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)

    def draw_gameover_scene(self):
        '''Prepare effects for gameover scene'''
        draw_list(bullet_list)
        draw_list(enemy_list)
        draw_list(blast_list)
        pyxel.text(43, 66, "GAMEOVER", 8)
        pyxel.text(31, 126, "- PRESS ENTER -", 13)


App()
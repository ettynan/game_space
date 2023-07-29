import unittest
from unittest.mock import patch, MagicMock
from player.model import Player, PLAYER_SPEED, PLAYER_WIDTH, \
    PLAYER_HEIGHT

class TestPlayer(unittest.TestCase):
    def setUp(self):
        '''Reset button states at the start of each test'''
        self.mock_pyxel = MagicMock()
        self.mock_pyxel.width = 200
        self.mock_pyxel.height = 200
        self.mock_pyxel.KEY_LEFT = 1
        self.mock_pyxel.KEY_RIGHT = 2
        self.mock_pyxel.KEY_UP = 3
        self.mock_pyxel.KEY_DOWN = 4
        self.mock_pyxel.KEY_SPACE = 5
        self.mock_pyxel.btn.reset_mock()
        self.mock_pyxel.btnp.reset_mock()
        self.player = Player(50, 50)

    def test_update_move_left(self):
        '''Test that the player moves left when left arrow key is pressed'''
        self.mock_pyxel.btn.side_effect = lambda key: key == \
            self.mock_pyxel.KEY_LEFT
        with patch('player.model.pyxel', self.mock_pyxel):
            self.player.update()
        self.assertEqual(self.player.x, 50 - PLAYER_SPEED)

    def test_update_move_right(self):
        '''Test that the player moves right when right arrow key is pressed'''
        self.mock_pyxel.btn.side_effect = lambda key: key == \
            self.mock_pyxel.KEY_RIGHT
        with patch('player.model.pyxel', self.mock_pyxel):
            self.player.update()
        self.assertEqual(self.player.x, 50 + PLAYER_SPEED)

    def test_update_move_up(self):
        '''Test that the player moves up when up arrow key is pressed'''
        self.mock_pyxel.btn.side_effect = lambda key: key == \
            self.mock_pyxel.KEY_UP
        with patch('player.model.pyxel', self.mock_pyxel):
            self.player.update()
        self.assertEqual(self.player.y, 50 - PLAYER_SPEED)

    def test_update_move_down(self):
        '''Test that the player moves down when down arrow key is pressed'''
        self.mock_pyxel.btn.side_effect = lambda key: key == \
            self.mock_pyxel.KEY_DOWN
        with patch('player.model.pyxel', self.mock_pyxel):
            self.player.update()
        self.assertEqual(self.player.y, 50 + PLAYER_SPEED)

    def test_bullet_creation(self):
        '''Tests that the bullt is created as expected when player hits space'''
        # Simulate pressing the space key
        self.mock_pyxel.btnp.return_value = True
        self.mock_pyxel.KEY_SPACE = True
        with patch('player.model.Bullet', autospec=True) as mock_bullet, \
             patch('player.model.pyxel', self.mock_pyxel):
            self.player.update()
        # Test if the bullet was created when the space key was pressed
        mock_bullet.assert_called_once()

    def test_draw(self):
        '''Test the draw method of the player'''
        with patch('player.model.pyxel', self.mock_pyxel):
            self.player.draw()
        self.mock_pyxel.blt.assert_called_once_with(50, 50, 0, 0, 0, \
            PLAYER_WIDTH, PLAYER_HEIGHT, 0)

if __name__ == '__main__':
    unittest.main()

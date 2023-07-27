import unittest
from unittest.mock import patch
from enemy.model import Enemy, ENEMY_WIDTH, ENEMY_HEIGHT, ENEMY_SPEED

class TestEnemy(unittest.TestCase):

    @patch('enemy.model.random')
    @patch('enemy.model.pyxel')
    def setUp(self, mock_pyxel, mock_random):
        mock_pyxel.width = 100
        mock_pyxel.height = 100
        mock_random.return_value = 0.5
        self.enemy = Enemy(50, 50)

    def test_init(self):
        self.assertEqual(self.enemy.x, 50)
        self.assertEqual(self.enemy.y, 50)
        self.assertEqual(self.enemy.w, ENEMY_WIDTH)
        self.assertEqual(self.enemy.h, ENEMY_HEIGHT)
        self.assertEqual(self.enemy.dir, 1)
        self.assertEqual(self.enemy.alive, True)
        self.assertEqual(self.enemy.offset, 30)
        self.assertIn(self.enemy, Enemy.enemy_list)

    @patch('enemy.model.pyxel')
    def test_update(self, mock_pyxel):
        mock_pyxel.height = 100
        mock_pyxel.frame_count = 60

        self.enemy.update()

        self.assertEqual(self.enemy.y, 50 + ENEMY_SPEED)
        self.assertEqual(self.enemy.x, 50 - ENEMY_SPEED)

    @patch('enemy.model.pyxel')
    def test_draw(self, mock_pyxel):
        self.enemy.draw()
        mock_pyxel.blt.assert_called_with(self.enemy.x, self.enemy.y, 0, 8, 0,
                                          self.enemy.w * self.enemy.dir,
                                          self.enemy.h, 0)

if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import patch, PropertyMock, MagicMock
from bullet.model import Bullet, BULLET_SPEED, BULLET_HEIGHT

class TestBullet(unittest.TestCase):
    def setUp(self):
        self.mock_pyxel = MagicMock()
        self.bullet = Bullet(10, 10)
        self.bullet.bullet_list = []  # clear bullet_list for each test

    def test_init(self):
        '''Test the creation of a bullet'''
        new_bullet = Bullet(20, 20)
        self.assertEqual(new_bullet.x, 20)
        self.assertEqual(new_bullet.y, 20)
        self.assertEqual(new_bullet.w, 2)  # BULLET_WIDTH
        self.assertEqual(new_bullet.h, 8)  # BULLET_HEIGHT
        self.assertTrue(new_bullet.alive)
        self.assertIn(new_bullet, new_bullet.bullet_list)

    def test_update(self):
        '''Test bullet movement and boundary conditions'''
        # mock pyxel.height property
        type(self.mock_pyxel).height = PropertyMock(return_value=100)
        with patch('bullet.model.pyxel', self.mock_pyxel):
            self.bullet.update()
        # After update, the y position of the bullet should decrease
        self.assertEqual(self.bullet.y, 10 - BULLET_SPEED)
        # Bullet that goes beyond top screen border should be marked not alive
        self.bullet.y = -BULLET_HEIGHT
        self.bullet.update()
        self.assertFalse(self.bullet.alive)

    def test_draw(self):
        '''Test the bullet drawing'''
        with patch('bullet.model.pyxel', self.mock_pyxel):
            self.bullet.draw()
        self.mock_pyxel.rect.assert_called_once_with(self.bullet.x, \
            self.bullet.y, self.bullet.w, self.bullet.h, 11)

if __name__ == '__main__':
    unittest.main()

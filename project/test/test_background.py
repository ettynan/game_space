'''Module to test the project.background.model module'''
import unittest
from unittest.mock import patch
from background.model import Background

class TestBackground(unittest.TestCase):

    @patch('background.model.random')
    @patch('background.model.pyxel')
    def setUp(self, mock_pyxel, mock_random):
        mock_pyxel.width = 100
        mock_pyxel.height = 100
        mock_random.return_value = 0.5
        self.background = Background()

    @patch('background.model.random')
    @patch('background.model.pyxel')
    def test_init(self, mock_pyxel, mock_random):
        mock_pyxel.width = 100
        mock_pyxel.height = 100
        mock_random.return_value = 0.5

        background = Background()
        self.assertEqual(len(background.star_list), background.STAR_COUNT)
        for star in background.star_list:
            x, y, speed = star
            self.assertEqual(x, 0.5 * mock_pyxel.width)
            self.assertEqual(y, 0.5 * mock_pyxel.height)
            self.assertEqual(speed, 0.5 * 1.5 + 1)

    @patch('background.model.pyxel')
    def test_update(self, mock_pyxel):
        mock_pyxel.height = 100

        self.background.update()
        for star in self.background.star_list:
            x, y, speed = star
            self.assertLess(y, mock_pyxel.height)

    @patch('background.model.pyxel')
    def test_draw(self, mock_pyxel):
        self.background.draw()

        mock_pyxel.pset.assert_called()
        for star in self.background.star_list:
            x, y, speed = star
            color = self.background.STAR_COLOR_HIGH if speed > 1.8 \
                else self.background.STAR_COLOR_LOW
            mock_pyxel.pset.assert_any_call(x, y, color)

if __name__ == "__main__":
    unittest.main()

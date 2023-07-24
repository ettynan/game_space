import unittest
from unittest.mock import patch
from blast.model import Blast, BLAST_START_RADIUS, BLAST_END_RADIUS

class TestBlast(unittest.TestCase):
    def setUp(self):
        '''Setting up for the test'''
        self.x = 10
        self.y = 20
        self.blast = Blast(self.x, self.y)

    def test_init(self):
        '''Testing the __init__ method'''
        self.assertEqual(self.blast.x, self.x)
        self.assertEqual(self.blast.y, self.y)
        self.assertEqual(self.blast.radius, BLAST_START_RADIUS)
        self.assertTrue(self.blast.alive)
        self.assertIn(self.blast, Blast.blast_list)

    def test_update(self):
        '''Testing the update method'''
        self.blast.update()
        self.assertEqual(self.blast.radius, BLAST_START_RADIUS + 1)

        # Simulate reaching the end radius
        self.blast.radius = BLAST_END_RADIUS
        self.blast.update()
        self.assertFalse(self.blast.alive)

    @patch('blast.model.pyxel.circb')
    @patch('blast.model.pyxel.circ')
    # Decorators are applied from the bottom up, check order
    def test_draw(self, mock_circ, mock_circb):
        '''Testing the draw method'''
        self.blast.draw()
        mock_circ.assert_called_once_with(self.x, self.y, self.blast.radius,
                                          self.blast.BLAST_COLOR_IN)
        mock_circb.assert_called_once_with(self.x, self.y, self.blast.radius,
                                           self.blast.BLAST_COLOR_OUT)


if __name__ == '__main__':
    unittest.main()

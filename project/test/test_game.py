import unittest
import pyxel
from game import App, SCENE_PLAY, SCENE_GAMEOVER, SCENE_TITLE

def setup_module(module):
    pyxel.init(120, 160)

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = App()

    def test_update_play_scene(self):
        self.app.scene = SCENE_PLAY
        self.app.update_play_scene()
        self.assertEqual(self.app.scene, SCENE_PLAY)

    def test_update_title_scene(self):
        self.app.scene = SCENE_TITLE
        self.app.update_title_scene()
        self.assertEqual(self.app.scene, SCENE_TITLE)

    def test_update_gameover_scene(self):
        self.app.scene = SCENE_GAMEOVER
        self.app.update()
        self.assertEqual(self.app.scene, SCENE_GAMEOVER)

if __name__ == "__main__":
    unittest.main()

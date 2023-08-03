import unittest
import os
import pyxel
from game import App, SCENE_PLAY, SCENE_GAMEOVER, SCENE_TITLE

os.environ["SDL_VIDEODRIVER"] = "dummy"

def setup_module(module):
    import os
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    pyxel.init(120, 160, title="All your base are belong to us!")

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

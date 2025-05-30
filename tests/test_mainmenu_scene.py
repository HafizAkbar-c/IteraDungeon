import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
)

import unittest
from unittest.mock import Mock, patch
import pygame

from scripts.scenes.mainmenu_scene import MainMenuScene


class TestMainMenuScene(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.mock_game = Mock()
        self.mock_game.screen = Mock()
        self.mock_game.screen.get_width.return_value = 800
        self.mock_game.screen.get_height.return_value = 600
        self.scene = MainMenuScene(self.mock_game)

    def tearDown(self):
        pygame.quit()

    def test_instantiation(self):
        self.assertIsInstance(self.scene, MainMenuScene)

    def test_handle_events_quit(self):
        # Should not raise
        self.scene.handle_events()

    def test_update(self):
        # Should not raise
        self.scene.update()

    def test_render(self):
        # Should not raise
        self.scene.render()


if __name__ == "__main__":
    unittest.main()

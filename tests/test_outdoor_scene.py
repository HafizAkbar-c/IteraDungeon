import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
)

import unittest
from unittest.mock import Mock, patch
import pygame

from scripts.scenes.outdoor_scene import OutdoorScene


class TestOutdoorScene(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.mock_game = Mock()
        self.mock_game.screen = Mock()
        self.mock_game.screen.get_width.return_value = 800
        self.mock_game.screen.get_height.return_value = 600
        self.mock_game.player = Mock()
        self.mock_game.player.player_size = [50, 50]
        self.scene = OutdoorScene(self.mock_game)

    def tearDown(self):
        pygame.quit()

    def test_instantiation(self):
        self.assertIsInstance(self.scene, OutdoorScene)

    def test_handle_events(self):
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

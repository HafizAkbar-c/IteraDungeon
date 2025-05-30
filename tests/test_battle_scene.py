import sys
import os

sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../scripts"))
)

import unittest
from unittest.mock import Mock, patch
import pygame

from scripts.scenes.battle_scene.battle_scene import BattleScene


class TestBattleScene(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.mock_game = Mock()
        self.mock_game.screen = pygame.Surface((800, 600))
        self.mock_game.clock = Mock()
        self.mock_game.clock.get_time.return_value = 0
        self.mock_game.player = Mock()
        self.mock_game.player.update = Mock()
        self.mock_game.player.hp = 100
        self.mock_game.player.current_skill = Mock()
        self.mock_game.player.current_ultimate = Mock()
        self.mock_game.player.set_floor_abilities = Mock()
        self.mock_game.player.skill_cooldown = 0
        self.mock_game.player.ultimate_cooldown = 0
        self.mock_enemy = Mock()
        self.mock_enemy.hp = 100
        self.mock_enemy.enemy_type = "Goblin"
        self.scene = BattleScene(self.mock_game, self.mock_enemy)
        # Patch center_enemy_frames to avoid NoneType error in render
        self.scene.center_enemy_frames = [pygame.Surface((100, 100))]
        self.scene.current_enemy_frame = 0
        self.scene.enemy_frame_timer = 0
        self.scene.enemy_frame_interval = 1000

    def tearDown(self):
        pygame.quit()

    def test_instantiation(self):
        self.assertIsInstance(self.scene, BattleScene)

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

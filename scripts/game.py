import pygame
from scene_manager import SceneManager
from player import Player
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Itera Dungeon")
        logo = pygame.image.load("scripts/assets/logo.png")
        pygame.display.set_icon(logo)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Player()
        self.scene_manager = SceneManager(self)

    def run(self):
        while self.running:
            self.scene_manager.handle_events()
            self.scene_manager.update()
            self.scene_manager.render()
            pygame.display.flip()
            self.clock.tick(FPS)

    def quit(self):
        self.running = False
        pygame.quit()

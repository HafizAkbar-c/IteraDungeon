import pygame
from scenes.base_scene import BaseScene
from scenes.options_scene import OptionsScene
from scenes.outdoor_scene import OutdoorScene

from utils.font_helper import FontHelper


class MainMenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = FontHelper.getFont("Minecraft", 48)
        self.options = ["Start", "Rename", "Exit"]
        self.selected = 0

        # Load and play main menu background music
        self.main_menu_music = pygame.mixer.Sound("scripts/assets/audio/main menu.mp3")
        self.main_menu_music.set_volume(0.5)  # Set volume to 50%
        self.main_menu_music.play(-1)  # Loop indefinitely

        self.background = pygame.image.load(
            "scripts/assets/Background/main_menu_scene.png"
        )
        self.background = pygame.transform.scale(
            self.background,
            (self.game.screen.get_width(), self.game.screen.get_height()),
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()

    def select_option(self):
        selected_option = self.options[self.selected]
        if selected_option == "Start":
            self.main_menu_music.stop()  # Stop main menu music
            outdoor_scene = OutdoorScene(self.game)
            self.game.scene_manager.go_to(outdoor_scene)
        elif selected_option == "Rename":
            self.main_menu_music.stop()  # Stop main menu music
            self.game.scene_manager.go_to(OptionsScene(self.game))
        elif selected_option == "Exit":
            self.main_menu_music.stop()  # Stop main menu music
            self.game.running = False

    def on_exit(self):
        # Stop main menu music when exiting the scene
        self.main_menu_music.stop()
        super().on_exit()

    def render(self):
        self.game.screen.blit(self.background, (0, 0))

        screen_width = self.game.screen.get_width()
        screen_height = self.game.screen.get_height()
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            text_rect = text.get_rect(
                center=(screen_width // 2, screen_height // 2 + i * 60)
            )
            self.game.screen.blit(text, text_rect)

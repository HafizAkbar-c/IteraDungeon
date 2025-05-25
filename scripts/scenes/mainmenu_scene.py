import pygame
from scenes.base_scene import BaseScene
from utils.font_helper import FontHelper


class MainMenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.stop()
        self.font = FontHelper.getFont("Minecraft", 48)
        self.options = ["Start", "Exit"]
        self.selected = 0
        self.main_menu_music = pygame.mixer.Sound("scripts/assets/audio/main menu.mp3")
        self.main_menu_music.set_volume(0.5)
        self.main_menu_music.play(-1)
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
                    if self.options[self.selected] == "Start":
                        from scenes.outdoor_scene import OutdoorScene

                        self.game.change_scene(OutdoorScene(self.game))
                    elif self.options[self.selected] == "Exit":
                        self.game.running = False

    def update(self):
        pass

    def render(self):
        self.game.screen.blit(self.background, (0, 0))

        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            rect = text.get_rect(
                center=(self.game.screen.get_width() // 2, 300 + i * 60)
            )
            self.game.screen.blit(text, rect)

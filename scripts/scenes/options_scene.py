import pygame
from scenes.base_scene import BaseScene


class OptionsScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 36)
        self.title_font = pygame.font.SysFont(None, 48)
        self.input_text = game.player.name
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_rate = 30
        self.message = ""
        self.message_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(self.input_text.strip()) > 0:
                        self.game.player.name = self.input_text.strip()
                        self.message = "Name saved successfully!"
                        self.message_timer = 90
                    else:
                        self.message = "Name cannot be empty!"
                        self.message_timer = 90
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                    self.message = ""
                elif event.key == pygame.K_ESCAPE:
                    from scenes.mainmenu_scene import MainMenuScene

                    self.game.scene_manager.go_to(MainMenuScene(self.game))
                else:
                    if len(self.input_text) < 20 and event.unicode.isprintable():
                        self.input_text += event.unicode
                        self.message = ""

    def update(self):
        self.cursor_timer += 1
        if self.cursor_timer >= self.cursor_blink_rate:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                if self.message == "Name saved successfully!":
                    from scenes.mainmenu_scene import MainMenuScene

                    self.game.scene_manager.go_to(MainMenuScene(self.game))

    def render(self):
        self.game.screen.fill((40, 40, 40))

        title_text = self.title_font.render("Rename Character", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.game.screen.get_width() // 2, 80))
        self.game.screen.blit(title_text, title_rect)

        pygame.draw.rect(
            self.game.screen,
            (60, 60, 60),
            pygame.Rect(100, 150, 600, 50),
            border_radius=5,
        )

        cursor = "|" if self.cursor_visible else ""
        name_text = self.font.render(self.input_text + cursor, True, (255, 255, 0))
        self.game.screen.blit(name_text, (110, 160))

        helper_text = self.font.render(
            "Press ENTER to save, ESC to cancel", True, (200, 200, 200)
        )
        helper_rect = helper_text.get_rect(
            center=(self.game.screen.get_width() // 2, 230)
        )
        self.game.screen.blit(helper_text, helper_rect)

        if self.message:
            message_color = (
                (0, 255, 0)
                if self.message == "Name saved successfully!"
                else (255, 100, 100)
            )
            message_text = self.font.render(self.message, True, message_color)
            message_rect = message_text.get_rect(
                center=(self.game.screen.get_width() // 2, 280)
            )
            self.game.screen.blit(message_text, message_rect)

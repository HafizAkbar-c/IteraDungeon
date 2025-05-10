import pygame
import time
from scenes.base_scene import BaseScene


class StoryTransitionScene(BaseScene):
    def __init__(self, game, story_text, next_scene=None, delay_per_line=2.0):
        super().__init__(game)
        self.story_text = story_text
        self.next_scene = next_scene
        self.font = pygame.font.SysFont(None, 28)
        self.current_line = 0
        self.finished = False
        self.start_time = time.time()
        self.fade_alpha = 255
        self.fade_state = "in"
        self.max_line_width = 700
        self.line_spacing = 30

        self.calculate_display_times()

    def calculate_display_times(self):
        self.display_times = []
        base_time = 1.0

        for line in self.story_text:
            if not line:
                self.display_times.append(0.5)
                continue

            char_count = len(line)
            reading_time = (char_count / 25) + base_time

            max_time = 3.0
            display_time = min(reading_time, max_time)

            self.display_times.append(display_time)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self.next_line()

    def next_line(self):
        if self.current_line < len(self.story_text) - 1:
            self.current_line += 1
            self.start_time = time.time()
            self.fade_alpha = 255
            self.fade_state = "in"
        else:
            self.finished = True
            self.fade_state = "out"

    def update(self):
        current_time = time.time()
        time_elapsed = current_time - self.start_time

        current_display_time = (
            self.display_times[self.current_line]
            if self.current_line < len(self.display_times)
            else 1.0
        )

        if self.fade_state == "in":
            self.fade_alpha = max(0, 255 - (time_elapsed * 1020))
            if self.fade_alpha <= 0:
                self.fade_state = "show"
                self.fade_alpha = 0

        elif self.fade_state == "show":
            if time_elapsed > current_display_time:
                self.fade_state = "out"

        elif self.fade_state == "out":
            self.fade_alpha = min(255, (time_elapsed - current_display_time) * 1020)
            if self.fade_alpha >= 255:
                if self.finished and self.next_scene:
                    self.game.scene_manager.go_to(self.next_scene)
                else:
                    self.next_line()

    def render(self):
        self.game.screen.fill((0, 0, 0))

        if self.current_line < len(self.story_text):
            current_text = self.story_text[self.current_line]

            text_lines = self.wrap_text(current_text, self.max_line_width)

            total_height = len(text_lines) * self.line_spacing
            start_y = (self.game.screen.get_height() - total_height) // 2

            for i, line in enumerate(text_lines):
                if line:
                    y_position = start_y + (i * self.line_spacing)
                    text_surface = self.font.render(line, True, (255, 255, 255))
                    text_rect = text_surface.get_rect(
                        center=(self.game.screen.get_width() // 2, y_position)
                    )
                    self.game.screen.blit(text_surface, text_rect)

        fade_surface = pygame.Surface(
            (self.game.screen.get_width(), self.game.screen.get_height())
        )
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(self.fade_alpha)
        self.game.screen.blit(fade_surface, (0, 0))

    def wrap_text(self, text, max_width):
        if not text:
            return [""]

        text_width, _ = self.font.size(text)

        if text_width <= max_width:
            return [text]
        else:
            words = text.split()
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + " " + word if current_line else word
                test_width, _ = self.font.size(test_line)

                if test_width <= max_width:
                    current_line = test_line
                else:
                    lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            return lines

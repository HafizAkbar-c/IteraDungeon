import pygame
import time


class UltimateAnimationManager:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_showing_ultimate = False
        self.ultimate_frame = 0
        self.ultimate_frames = []
        self.ultimate_start_time = 0
        self.ultimate_duration = 1.0
        self.pending_ultimate_damage = 0
        self.ultimate_completed = False

    def start_ultimate_animation(self, frame_paths, damage, duration):
        self.ultimate_frames = []
        for frame_path in frame_paths:
            img = pygame.image.load(frame_path)
            img = pygame.transform.scale(img, (self.screen_width, self.screen_height))
            self.ultimate_frames.append(img)

        self.pending_ultimate_damage = damage
        self.ultimate_completed = False
        self.is_showing_ultimate = True
        self.ultimate_frame = 0
        self.ultimate_start_time = time.time()
        self.ultimate_duration = duration

    def update(self):
        if not self.is_showing_ultimate:
            return False, 0

        current_time = time.time()
        elapsed = current_time - self.ultimate_start_time

        if elapsed >= self.ultimate_duration:
            self.is_showing_ultimate = False
            if not self.ultimate_completed:
                self.ultimate_completed = True
                return True, self.pending_ultimate_damage
        else:
            frame_duration = self.ultimate_duration / len(self.ultimate_frames)
            self.ultimate_frame = min(
                int(elapsed / frame_duration), len(self.ultimate_frames) - 1
            )

        return False, 0

    def render(self, screen):
        if self.is_showing_ultimate and self.ultimate_frame < len(self.ultimate_frames):
            screen.blit(self.ultimate_frames[self.ultimate_frame], (0, 0))
            return True
        return False

import pygame


class Attack:
    def __init__(self, player, range=40, duration=300):
        self.player = player
        self.range = range
        self.duration = duration
        self.active = False
        self.start_time = 0

    def start(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def update(self):
        if self.active and pygame.time.get_ticks() - self.start_time > self.duration:
            self.active = False

    def get_hitbox(self):
        if not self.active:
            return None

        x, y = self.player.current_floor.player_pos
        direction = self.player.game.player.facing

        if direction == "right":
            return pygame.Rect(x + 40, y, self.range, 40)
        elif direction == "left":
            return pygame.Rect(x - self.range, y, self.range, 40)

        return None

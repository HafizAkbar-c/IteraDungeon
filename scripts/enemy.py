import pygame


class Enemy:
    def __init__(self, x, y, size=40):
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(self.x, self.y - size, self.size, self.size)
        self.hp = 100
        self.damage = 5
        self.color = (255, 50, 50)

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y - self.size

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def check_hit_by(self, hitbox):
        return hitbox and self.rect.colliderect(hitbox)

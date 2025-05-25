import pygame
from scripts.player import Character


class Enemy(Character):
    def __init__(self, x, y, size=40, name="Enemy", hp=100, atk=5, defense=0, speed=1):
        super().__init__(name, hp, atk, defense, speed)
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(self.x, self.y - size, self.size, self.size)
        self.color = (255, 50, 50)
        self.image = None
        self.enemy_type = None

    def attack(self):
        return self._atk

    def update(self, delta_time=0.1):
        self.rect.x = self.x
        self.rect.y = self.y - self.size

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        else:
            pygame.draw.rect(screen, self.color, self.rect)

    def check_hit_by(self, hitbox):
        return hitbox and self.rect.colliderect(hitbox)


class Goblin(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, size=200, name="Goblin", atk=5)
        self.enemy_type = "Goblin"
        self.image = pygame.image.load("scripts/assets/Boss/goblin.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))


class Orc(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, size=200, name="Orc", atk=8)
        self.enemy_type = "Orc"
        self.image = pygame.image.load(
            "scripts/assets/Background/Floor 2/per-frame ogre_00000.png"
        )
        self.image = pygame.transform.scale(self.image, (self.size, self.size))


class Dragon(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, size=80, name="Dragon", atk=12)
        self.enemy_type = "Dragon"

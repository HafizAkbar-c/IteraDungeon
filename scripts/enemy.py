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
        self.image = None
        self.enemy_type = None

    def update(self):
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
        super().__init__(x, y, size=200)
        self.enemy_type = "Goblin"
        self.damage = 5
        self.image = pygame.image.load("scripts/assets/Boss/goblin.png")
        self.image = pygame.transform.scale(self.image, (self.size, self.size))


class Orc(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, size=200)
        self.enemy_type = "Orc"
        self.damage = 8
        self.image = pygame.image.load(
            "scripts/assets/Background/Floor 2/per-frame ogre_00000.png"
        )
        self.image = pygame.transform.scale(self.image, (self.size, self.size))


class Dragon(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, size=80)
        self.enemy_type = "Dragon"
        self.damage = 12

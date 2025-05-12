import pygame
from skill import SkillTree, Skill, Ultimate


class Player:
    def __init__(self):
        self.name = "Player"
        self.hp = 100
        self.atk = 10
        self.defense = 5
        self.speed = 8
        self.skill_tree = SkillTree()
        self.rect = pygame.Rect(100, 400, 32, 32)
        self.facing = "right"
        self.attack_active = False
        self.attack_timer = 0
        self.is_jumping = False
        self.current_skill = None
        self.current_ultimate = None
        self.skill_cooldown = 0
        self.ultimate_cooldown = 0

        # Player images
        self.player_size = (200, 200)
        self._player_front = None
        self._player_right = None
        self._player_left = None
        self._player_attack = None
        self._load_images()

    def _load_images(self):
        # Load player images
        self._player_front = pygame.image.load(
            "scripts/assets/Main Character/front_facing.png"
        )
        self._player_right = pygame.image.load(
            "scripts/assets/Main Character/right_facing.png"
        )
        self._player_left = pygame.image.load(
            "scripts/assets/Main Character/left_facing.png"
        )
        self._player_attack = pygame.image.load(
            "scripts/assets/Main Character/ambush.png"
        )

        # Scale images
        self._player_front = pygame.transform.scale(
            self._player_front, self.player_size
        )
        self._player_right = pygame.transform.scale(
            self._player_right, self.player_size
        )
        self._player_left = pygame.transform.scale(self._player_left, self.player_size)
        self._player_attack = pygame.transform.scale(
            self._player_attack, self.player_size
        )

    @property
    def front_image(self):
        return self._player_front

    @property
    def right_image(self):
        return self._player_right

    @property
    def left_image(self):
        return self._player_left

    @property
    def attack_image(self):
        return self._player_attack

    def attack(self):
        self.attack_active = True
        self.attack_timer = 10
        return self.atk

    def use_skill(self):
        if self.current_skill and self.skill_cooldown <= 0:
            damage = self.current_skill.use()
            self.skill_cooldown = self.current_skill.cooldown
            return damage
        return 0

    def use_ultimate(self):
        if self.current_ultimate and self.ultimate_cooldown <= 0:
            damage = self.current_ultimate.use()
            self.ultimate_cooldown = self.current_ultimate.cooldown
            return damage
        return 0

    def update(self, delta_time=0.1):
        if self.attack_active:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.attack_active = False
        if self.skill_cooldown > 0:
            self.skill_cooldown -= delta_time
        if self.ultimate_cooldown > 0:
            self.ultimate_cooldown -= delta_time
        if self.current_skill:
            self.current_skill.update(delta_time)
        if self.current_ultimate:
            self.current_ultimate.update(delta_time)

    def set_floor_abilities(self, floor_index):
        if floor_index == 0:
            self.current_skill = Skill(
                "Fireball",
                damage=15,
                cooldown=3.0,
                description="Fire damage that burns the enemy",
            )
            self.current_ultimate = Ultimate(
                "Meteor",
                damage=30,
                cooldown=5.0,
                description="Massive fire explosion from the sky",
            )
        elif floor_index == 1:
            self.current_skill = Skill(
                "Ice Spike",
                damage=18,
                cooldown=3.0,
                description="Ice damage with slowdown effect",
            )
            self.current_ultimate = Ultimate(
                "Blizzard",
                damage=35,
                cooldown=5.0,
                description="Freezes all enemies in the area",
            )
        elif floor_index == 2:
            self.current_skill = Skill(
                "Lightning Bolt",
                damage=20,
                cooldown=3.0,
                description="Electric damage that paralyzes",
            )
            self.current_ultimate = Ultimate(
                "Thunderstorm",
                damage=40,
                cooldown=5.0,
                description="Chain lightning that hits multiple times",
            )

    @property
    def attack_rect(self):
        offset = 20
        if self.facing == "right":
            return pygame.Rect(self.rect.right, self.rect.top, offset, self.rect.height)
        elif self.facing == "left":
            return pygame.Rect(
                self.rect.left - offset, self.rect.top, offset, self.rect.height
            )
        elif self.facing == "up":
            return pygame.Rect(
                self.rect.left, self.rect.top - offset, self.rect.width, offset
            )
        elif self.facing == "down":
            return pygame.Rect(
                self.rect.left, self.rect.bottom, self.rect.width, offset
            )

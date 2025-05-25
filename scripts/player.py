import pygame
from skill import (
    SkillTree,
    Skill,
    FireUltimate,
    IceUltimate,
    LightningUltimate,
)


class Character:
    def __init__(self, name, hp, atk, defense, speed):
        self._name = name
        self._hp = hp
        self._atk = atk
        self._defense = defense
        self._speed = speed

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = max(0, value)

    @property
    def atk(self):
        return self._atk

    @property
    def defense(self):
        return self._defense

    @property
    def speed(self):
        return self._speed

    def attack(self):
        pass

    def update(self, delta_time=0.1):
        pass


class Player(Character):
    def __init__(self):
        super().__init__("Player", 100, 10, 5, 8)
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
        self.attack_frame = 0
        self.attack_counter = 0
        self.attack_frame_delay = 6
        self.walk_frame = 0
        self.walk_counter = 0
        self.walk_frame_delay = 6

        self.player_size = (200, 200)
        self._player_front = None
        self._player_right = None
        self._player_left = None
        self._player_attack = None
        self._load_images()

    def get_walk_frame(self):
        self.walk_counter += 1
        if self.walk_counter >= self.walk_frame_delay:
            self.walk_counter = 0
            self.walk_frame = (self.walk_frame + 1) % len(self.walk_right_images)
        return self.walk_right_images[self.walk_frame]

    def get_attack_frame(self):
        self.attack_counter += 1
        if self.attack_counter >= self.attack_frame_delay:
            self.attack_counter = 0
            self.attack_frame += 1
            if self.attack_frame >= len(self.attack_images):
                self.attack_frame = 0
                self.attack_active = False
        return self.attack_images[self.attack_frame]

    def _load_images(self):
        self._player_front = pygame.image.load(
            "scripts/assets/Main Character/front_facing.png"
        )
        self.walk_right_images = []
        for i in range(3):
            img = pygame.image.load(f"scripts/assets/Main Character/jalan0000{i}.png")
            img = pygame.transform.scale(img, self.player_size)
            self.walk_right_images.append(img)

        self.walk_left_images = [
            pygame.transform.flip(img, True, False) for img in self.walk_right_images
        ]

        self.attack_images = []
        for i in range(3):
            img = pygame.image.load(f"scripts/assets/Main Character/Action_0000{i}.png")
            img = pygame.transform.scale(img, self.player_size)
            self.attack_images.append(img)

        self._player_front = pygame.transform.scale(
            self._player_front, self.player_size
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
            self.current_ultimate = FireUltimate(
                damage=30,
                cooldown=20.0,
            )
        elif floor_index == 1:
            self.current_skill = Skill(
                "Ice Spike",
                damage=18,
                cooldown=3.0,
                description="Ice damage with slowdown effect",
            )
            self.current_ultimate = IceUltimate(
                damage=35,
                cooldown=5.0,
            )
        elif floor_index == 2:
            self.current_skill = Skill(
                "Lightning Bolt",
                damage=20,
                cooldown=3.0,
                description="Electric damage that paralyzes",
            )
            self.current_ultimate = LightningUltimate(
                damage=40,
                cooldown=5.0,
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

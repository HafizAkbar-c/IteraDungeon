import os
from abc import ABC, abstractmethod


class BaseSkill(ABC):
    def __init__(self, name, damage=0, cooldown=3.0, description=""):
        self._name = name
        self._damage = damage
        self._cooldown = cooldown
        self._description = description
        self._cooldown_remaining = 0

    @property
    def name(self):
        return self._name

    @property
    def damage(self):
        return self._damage

    @property
    def cooldown(self):
        return self._cooldown

    @property
    def description(self):
        return self._description

    @abstractmethod
    def use(self):
        pass

    def update(self, delta_time=0.016):
        if self._cooldown_remaining > 0:
            self._cooldown_remaining -= delta_time


class Skill(BaseSkill):
    def __init__(
        self,
        name,
        damage=0,
        cooldown=3.0,
        description="",
        unlocked=False,
        required_level=1,
    ):
        super().__init__(name, damage, cooldown, description)
        self.unlocked = unlocked
        self.required_level = required_level

    def can_unlock(self, player_level):
        return player_level >= self.required_level and not self.unlocked

    def unlock(self):
        self.unlocked = True

    def use(self):
        if self._cooldown_remaining <= 0:
            self._cooldown_remaining = self._cooldown
            return self._damage
        return 0


class Ultimate(BaseSkill):
    def __init__(self, name, damage=0, cooldown=5.0, description=""):
        super().__init__(name, damage, cooldown, description)
        self.frames = []
        self.animation_duration = 1.0
        self._load_frames()

    def _load_frames(self):
        pass

    def get_frames(self):
        return self.frames

    def use(self):
        if self._cooldown_remaining <= 0:
            self._cooldown_remaining = self._cooldown
            return self._damage
        return 0

class FireSkill(Skill):
    def __init__(self, damage=15, cooldown=3.0):
        super().__init__(
            "Fireball", damage, cooldown, "Api Yang Membakar Musuh"
        )

class IceSkill(Skill):
    def __init__(self, damage=18, cooldown=3.0):
        super().__init__(
            "Ice Spike", damage, cooldown, "Es yang Membekukan Musuh"
        )

class LightningSkill(Skill):
    def __init__(self, damage=20, cooldown=3.0):
        super().__init__(
            "Lightning Bolt", damage, cooldown, "Listrik yang Menyambar Musuh"
        )

class FireUltimate(Ultimate):
    def __init__(self, damage=30, cooldown=5.0):
        super().__init__(
            "Meteor", damage, cooldown, "Massive fire explosion from the sky"
        )

    def _load_frames(self):
        self.frames = []
        base_path = "scripts/assets/Main Character/Ulti"
        frames_files = [
            "ulti-frame-1.jpg",
            "ulti-frame-2.jpg",
            "ulti-frame-3.jpg",
            "ulti-frame-4.jpg",
            "ulti-frame-5.jpg",
            "ulti-frame-6.jpg",
        ]
        
        for frame_file in frames_files:
            frame_path = os.path.join(base_path, frame_file)
            if os.path.exists(frame_path):
                self.frames.append(frame_path)

class IceUltimate(Ultimate):
    def __init__(self, damage=35, cooldown=5.0):
        super().__init__(
            "Blizzard", damage, cooldown, "Freezes all enemies in the area"
        )
    def _load_frames(self):
        self.frames = []
        base_path = "scripts/assets/Main Character/Ulti 2"
        frames_files = [
            "Ulti 2_00000.png",
            "Ulti 2_00007.png",
            "Ulti 2_00014.png",
            "Ulti 2_00021.png",
            "Ulti 2_00028.png",
            "Ulti 2_00034.png",
        ]
        for frame_file in frames_files:
            frame_path = os.path.join(base_path, frame_file)
            if os.path.exists(frame_path):
                self.frames.append(frame_path)

class LightningUltimate(Ultimate):
    def __init__(self, damage=40, cooldown=5.0):
        super().__init__(
            "Thunderstorm", damage, cooldown, "Chain lightning that hits multiple times"
        )

    def _load_frames(self):
        self.frames = [
            "scripts/assets/Main Character/Ulti 3/ulti 3 perframe_00000.png",
            "scripts/assets/Main Character/Ulti 3/ulti 3 perframe_00006.png",
            "scripts/assets/Main Character/Ulti 3/ulti 3 perframe_00012.png",
            "scripts/assets/Main Character/Ulti 3/ulti 3 perframe_00018.png",
            "scripts/assets/Main Character/Ulti 3/ulti 3 perframe_00024.png",
            "scripts/assets/Main Character/Ulti 3/ulti 3 perframe_00032.png",
        ]


class SkillTree:
    def __init__(self):
        self.skills = [
            Skill(
                "Power Strike",
                damage=50,
                cooldown=10.0,
                description="Deal heavy damage.",
                required_level=2,
            ),
            Skill(
                "Swift Step",
                damage=0,
                cooldown=20.0,
                description="Increase speed for 3 turns.",
                required_level=3,
            ),
            Skill(
                "Iron Guard",
                damage=0,
                cooldown=20.0,
                description="Increase defense temporarily.",
                required_level=4,
            ),
        ]

    def get_unlockable_skills(self, player_level):
        return [skill for skill in self.skills if skill.can_unlock(player_level)]

    def unlock_skill(self, skill_name, player_level):
        for skill in self.skills:
            if skill.name == skill_name and skill.can_unlock(player_level):
                skill.unlock()
                return True
        return False

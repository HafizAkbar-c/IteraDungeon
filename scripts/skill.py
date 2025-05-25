import os


class Skill:
    def __init__(
        self,
        name,
        damage=0,
        cooldown=3.0,
        description="",
        unlocked=False,
        required_level=1,
    ):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.description = description
        self.unlocked = unlocked
        self.required_level = required_level
        self.cooldown_remaining = 0

    def can_unlock(self, player_level):
        return player_level >= self.required_level and not self.unlocked

    def unlock(self):
        self.unlocked = True

    def use(self):
        if self.cooldown_remaining <= 0:
            self.cooldown_remaining = self.cooldown
            return self.damage
        return 0

    def update(self, delta_time=0.016):
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= delta_time


class Ultimate:
    def __init__(self, name, damage=0, cooldown=5.0, description=""):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.description = description
        self.cooldown_remaining = 0
        self.frames = []
        self.animation_duration = 1.0
        self._load_frames()

    def _load_frames(self):
        pass

    def get_frames(self):
        return self.frames

    def use(self):
        if self.cooldown_remaining <= 0:
            self.cooldown_remaining = self.cooldown
            return self.damage
        return 0

    def update(self, delta_time=0.016):
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= delta_time


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

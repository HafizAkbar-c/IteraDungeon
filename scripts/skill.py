class Skill:
    def __init__(self, name, damage=0, cooldown=3.0, description="", unlocked=False):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown
        self.description = description
        self.unlocked = unlocked
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

    def use(self):
        if self.cooldown_remaining <= 0:
            self.cooldown_remaining = self.cooldown
            return self.damage
        return 0

    def update(self, delta_time=0.016):
        if self.cooldown_remaining > 0:
            self.cooldown_remaining -= delta_time


class SkillTree:
    def __init__(self):
        self.skills = [
            Skill(
                "Power Strike",
                damage=50,
                cooldown=3.0,
                description="Deal heavy damage.",
            ),
            Skill(
                "Swift Step",
                damage=0,
                cooldown=2.0,
                description="Increase speed for 3 turns.",
            ),
            Skill(
                "Iron Guard",
                damage=0,
                cooldown=4.0,
                description="Increase defense temporarily.",
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

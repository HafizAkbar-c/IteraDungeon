class BattleActionHandler:
    def __init__(self, player, enemy, exploration_scene, logger, punch_sound=None,fire_ultimate=None, ice_ultimate=None, lightning_ultimate=None, 
                fire_skill=None, ice_skill=None, lightning_skill=None):
        self.player = player
        self.enemy = enemy
        self.exploration_scene = exploration_scene
        self.logger = logger
        self.punch_sound = punch_sound
        self.turn = self._determine_initial_turn(exploration_scene, player_first=True)
        self.fire_skill = fire_skill
        self.ice_skill = ice_skill
        self.lightning_skill = lightning_skill
        self.fire_ultimate = fire_ultimate
        self.ice_ultimate = ice_ultimate
        self.lightning_ultimate = lightning_ultimate

    def _determine_initial_turn(self, exploration_scene, player_first):
        if exploration_scene and exploration_scene.current_floor:
            return exploration_scene.current_floor.current_turn
        return "player" if player_first else "enemy"

    def use_attack(self):
        if self.punch_sound:
            self.punch_sound.play()

        damage = self.player.attack()
        self.enemy.hp -= damage
        self.logger.add_to_battle_log(f"{self.player.name} menyerang! Damage: {damage}")

        if self.enemy.hp <= 0:
            self.enemy.hp = 0
            return

        damage = self.enemy.damage
        self.player.hp -= damage
        self.logger.add_to_battle_log(f"Musuh menyerang! Damage: {damage}")

        if self.exploration_scene and self.exploration_scene.current_floor:
            self.exploration_scene.current_floor.set_turn(self.turn)

    def use_skill(self):
        if self.player.skill_cooldown <= 0:
            damage = self.player.use_skill()
            if damage > 0:
                self.enemy.hp -= damage
                skill_name = self.player.current_skill.name
                if self.player.current_skill.name == "Fireball" and self.fire_skill:
                    self.fire_skill.play()
                elif self.player.current_skill.name == "Ice Spike" and self.ice_skill:
                    self.ice_skill.play()
                elif self.player.current_skill.name == "Lightning Bolt" and self.lightning_skill:
                    self.lightning_skill.play()
                self.player.skill_cooldown = self.player.current_skill.cooldown
                self.logger.add_to_battle_log(
                    f"{self.player.name} menggunakan {skill_name}! Damage: {damage}"
                )

                if self.enemy.hp <= 0:
                    self.enemy.hp = 0
                    return

                damage = self.enemy.damage
                self.player.hp -= damage
                self.logger.add_to_battle_log(f"Musuh menyerang! Damage: {damage}")

                if self.exploration_scene and self.exploration_scene.current_floor:
                    self.exploration_scene.current_floor.set_turn(self.turn)
            else:
                self.logger.add_to_battle_log("Skill sedang cooldown!")
        else:
            self.logger.add_to_battle_log(
                f"Skill masih cooldown: {self.player.skill_cooldown:.1f}s"
            )

    def use_ultimate(self):
        if self.player.ultimate_cooldown <= 0:
            damage = self.player.use_ultimate()
            if damage > 0:
                self.player.ultimate_cooldown = self.player.current_ultimate.cooldown
                if self.player.current_ultimate.name == "Meteor" and self.fire_ultimate:
                    self.fire_ultimate.play()
                elif self.player.current_ultimate.name == "Blizzard" and self.ice_ultimate:
                    self.ice_ultimate.play()
                elif self.player.current_ultimate.name == "Thunderstorm" and self.lightning_ultimate:
                    self.lightning_ultimate.play()
                ultimate_name = self.player.current_ultimate.name
                self.logger.add_to_battle_log(
                    f"{self.player.name} menggunakan {ultimate_name}!"
                )

                ultimate_frame_paths = self.player.current_ultimate.get_frames()
                return damage, ultimate_frame_paths
            else:
                self.logger.add_to_battle_log("Ultimate sedang cooldown!")
        else:
            self.logger.add_to_battle_log(
                f"Ultimate masih cooldown: {self.player.ultimate_cooldown:.1f}s"
            )
        return 0, []

    def process_ultimate_damage(self, damage):
        self.enemy.hp -= damage
        self.logger.add_to_battle_log(f"Damage: {damage}")

        if self.enemy.hp <= 0:
            self.enemy.hp = 0
            return

        damage = self.enemy.damage
        self.player.hp -= damage
        self.logger.add_to_battle_log(f"Musuh menyerang! Damage: {damage}")

        if self.exploration_scene and self.exploration_scene.current_floor:
            self.exploration_scene.current_floor.set_turn(self.turn)

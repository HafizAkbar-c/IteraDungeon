import pygame
from scenes.base_scene import BaseScene
from scenes.story_transition_scene import StoryTransitionScene


class BattleScene(BaseScene):
    def __init__(self, game, enemy, player_first=True, exploration_scene=None):
        super().__init__(game)
        self.enemy = enemy
        self.player_first = player_first

        if exploration_scene and exploration_scene.current_floor:
            self.turn = exploration_scene.current_floor.current_turn
            self.current_floor_index = exploration_scene.current_floor_index
        else:
            self.turn = "player" if player_first else "enemy"
            self.current_floor_index = 0

        self.font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 20)
        self.done = False
        self.exploration_scene = exploration_scene
        self.screen_width = game.screen.get_width()
        self.screen_height = game.screen.get_height()
        self.frame_margin = 40
        self.player_frame_size = (150, 150)
        self.player_frame_pos = (
            self.frame_margin,
            self.screen_height - 170,
        )

        self.enemy_frame_size = (150, 150)
        self.enemy_frame_pos = (
            self.screen_width - self.frame_margin - self.enemy_frame_size[0],
            self.screen_height - 170,
        )

        self.action_box_size = (300, 150)
        self.action_box_pos = (self.screen_width - 330, 20)
        self.log_margin_bottom = 15

        self.battle_log = [
            "Pertempuran dimulai!",
        ]
        self.max_log_entries = 8
        self.visible_log_entries = min(6, self.max_log_entries)
        self.log_scroll_position = 0

        self.button_width = 110
        self.button_height = 50
        self.button_margin = 25
        self.button_y = self.screen_height - 70
        self.selected_button = 0

        button_total_width = (self.button_width * 3) + (self.button_margin * 2)
        start_x = (self.screen_width - button_total_width) // 2

        self.attack_button_rect = pygame.Rect(
            start_x,
            self.button_y,
            self.button_width,
            self.button_height,
        )

        self.skill_button_rect = pygame.Rect(
            start_x + self.button_width + self.button_margin,
            self.button_y,
            self.button_width,
            self.button_height,
        )

        self.ultimate_button_rect = pygame.Rect(
            start_x + (self.button_width * 2) + (self.button_margin * 2),
            self.button_y,
            self.button_width,
            self.button_height,
        )

        if exploration_scene and exploration_scene.current_floor_index is not None:
            if (
                self.game.player.current_skill is None
                or self.game.player.current_ultimate is None
            ):
                self.game.player.set_floor_abilities(
                    exploration_scene.current_floor_index
                )

        # Load player and enemy images
        self.player_image = pygame.image.load(
            "scripts/assets/Main Character/front_facing.png"
        )
        self.player_image = pygame.transform.scale(self.player_image, (130, 130))
        
        # Load enemy images based on floor
        self.enemy_image = None
        if hasattr(self.enemy, "enemy_type"):
            if self.enemy.enemy_type == "Goblin":
                self.enemy_image = pygame.image.load("scripts/assets/Boss/goblin.png")
                self.enemy_image = pygame.transform.scale(self.enemy_image, (130, 130))
        
        # Center battle enemy image - make it larger for better visibility
        self.center_enemy_size = (200, 200)
        self.center_enemy_image = None
        if hasattr(self.enemy, "enemy_type"):
            if self.enemy.enemy_type == "Goblin":
                self.center_enemy_image = pygame.image.load("scripts/assets/Boss/goblin.png")
                self.center_enemy_image = pygame.transform.scale(self.center_enemy_image, self.center_enemy_size)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                if self.turn == "player":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if self.selected_button == 0:
                            self.use_attack()
                        elif self.selected_button == 1:
                            self.use_skill()
                        elif self.selected_button == 2:
                            self.use_ultimate()
                    elif event.key == pygame.K_LEFT:
                        self.selected_button = max(0, self.selected_button - 1)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_button = min(2, self.selected_button + 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.turn == "player":
                        if self.attack_button_rect.collidepoint(mouse_pos):
                            self.selected_button = 0
                            self.use_attack()
                        elif self.skill_button_rect.collidepoint(mouse_pos):
                            self.selected_button = 1
                            self.use_skill()
                        elif self.ultimate_button_rect.collidepoint(mouse_pos):
                            self.selected_button = 2
                            self.use_ultimate()

    def use_attack(self):
        damage = self.game.player.attack()
        self.enemy.hp -= damage
        self.add_to_battle_log(f"{self.game.player.name} menyerang! Damage: {damage}")

        if self.enemy.hp <= 0:
            self.enemy.hp = 0
            return

        damage = self.enemy.damage
        self.game.player.hp -= damage
        self.add_to_battle_log(f"Musuh menyerang! Damage: {damage}")

        if self.exploration_scene and self.exploration_scene.current_floor:
            self.exploration_scene.current_floor.set_turn(self.turn)

    def use_skill(self):
        if self.game.player.skill_cooldown <= 0:
            damage = self.game.player.use_skill()
            if damage > 0:
                self.enemy.hp -= damage
                skill_name = self.game.player.current_skill.name
                self.add_to_battle_log(
                    f"{self.game.player.name} menggunakan {skill_name}! Damage: {damage}"
                )

                if self.enemy.hp <= 0:
                    self.enemy.hp = 0
                    return

                damage = self.enemy.damage
                self.game.player.hp -= damage
                self.add_to_battle_log(f"Musuh menyerang! Damage: {damage}")

                if self.exploration_scene and self.exploration_scene.current_floor:
                    self.exploration_scene.current_floor.set_turn(self.turn)
            else:
                self.add_to_battle_log("Skill sedang cooldown!")
        else:
            self.add_to_battle_log(
                f"Skill masih cooldown: {self.game.player.skill_cooldown:.1f}s"
            )

    def use_ultimate(self):
        if self.game.player.ultimate_cooldown <= 0:
            damage = self.game.player.use_ultimate()
            if damage > 0:
                self.enemy.hp -= damage
                ultimate_name = self.game.player.current_ultimate.name
                self.add_to_battle_log(
                    f"{self.game.player.name} menggunakan {ultimate_name}! Damage: {damage}"
                )

                if self.enemy.hp <= 0:
                    self.enemy.hp = 0
                    return

                damage = self.enemy.damage
                self.game.player.hp -= damage
                self.add_to_battle_log(f"Musuh menyerang! Damage: {damage}")

                if self.exploration_scene and self.exploration_scene.current_floor:
                    self.exploration_scene.current_floor.set_turn(self.turn)
            else:
                self.add_to_battle_log("Ultimate sedang cooldown!")
        else:
            self.add_to_battle_log(
                f"Ultimate masih cooldown: {self.game.player.ultimate_cooldown:.1f}s"
            )

    def add_to_battle_log(self, message):
        self.battle_log.append(message)
        if len(self.battle_log) > self.max_log_entries:
            self.battle_log.pop(0)

        if len(self.battle_log) > self.visible_log_entries:
            self.log_scroll_position = len(self.battle_log) - self.visible_log_entries

    def update(self):
        self.game.player.update()

        if self.done:
            return

        if self.enemy.hp <= 0:
            self.add_to_battle_log("Kamu menang!")
            self.done = True

            if self.exploration_scene:
                if self.exploration_scene.current_floor:
                    self.exploration_scene.current_floor.set_turn(self.turn)

                if self.exploration_scene.current_floor_index == 2:
                    self.show_ending()
                else:
                    self.exploration_scene.on_battle_complete(enemy_defeated=True)
                    self.game.scene_manager.go_to(self.exploration_scene)
            else:
                from scenes.exploration_scene import ExplorationScene

                self.game.scene_manager.go_to(ExplorationScene(self.game))

        elif self.game.player.hp <= 0:
            self.add_to_battle_log("Kamu kalah! Game over.")
            self.done = True
            self.game.quit()

    def show_ending(self):
        ending_story = [
            "Naga yang mengerikan itu akhirnya jatuh ke tanah dengan dentuman keras.",
            "Kamu berdiri terengah-engah, nyaris tidak percaya bahwa kamu berhasil mengalahkannya.",
            "",
            "Tiba-tiba, dinding dungeon mulai bergetar dan retakan mulai muncul di dinding-dinding tua.",
            "Cahaya keemasan menembus dari celah-celah retakan di langit-langit.",
            "",
            "Suara misterius terdengar bergema dalam kepalamu:",
            '"Penakluk Dungeon ITERA, kau telah membersihkan kegelapan yang mengancam kampus."',
            "",
            "Kamu menutup mata, silau oleh cahaya yang semakin terang.",
            "Sensasi hangat menjalar ke seluruh tubuhmu, seolah-olah kamu melayang...",
            "",
            "Ketika kamu membuka mata kembali, kamu terkejut menemukan dirimu...",
            "...terbaring di bawah pohon rindang di taman kampus ITERA.",
            "",
            "Beberapa mahasiswa berlalu-lalang dan dosen mengajar seperti biasa.",
            "Seolah tidak terjadi apa-apa. Seolah petualanganmu hanyalah mimpi.",
            "",
            "Kamu melihat jam tanganmu - hanya 10 menit berlalu sejak orientasi kampus dimulai.",
            "",
            "Di sampingmu, kamu menemukan sebuah medali emas dengan ukiran naga.",
            "Bukti bahwa semua itu bukan sekadar mimpi belaka.",
            "",
            "Satu hal yang pasti: pengalamanmu di Dungeon ITERA telah mengubahmu.",
            "Kamu bukan lagi mahasiswa biasa...",
            "",
            "Kamu adalah Penakluk Dungeon ITERA, Pembebas Kegelapan, dan Pahlawan Tersembunyi kampus.",
            "",
            "TAMAT",
            "",
            "Terima kasih telah bermain!",
        ]

        from scenes.mainmenu_scene import MainMenuScene

        main_menu = MainMenuScene(self.game)

        ending_scene = StoryTransitionScene(
            self.game, ending_story, main_menu, delay_per_line=3.0
        )

        self.game.scene_manager.go_to(ending_scene)

    def render(self):
        self.game.screen.fill((0, 0, 0))

        # Draw center enemy with goblin image for first floor
        enemy_center_pos = (self.screen_width // 2, self.screen_height // 3)
        enemy_size = self.center_enemy_size
        enemy_rect = pygame.Rect(
            enemy_center_pos[0] - enemy_size[0] // 2,
            enemy_center_pos[1] - enemy_size[1] // 2,
            enemy_size[0],
            enemy_size[1],
        )
        
        # Draw the enemy image in the center
        if self.center_enemy_image:
            self.game.screen.blit(self.center_enemy_image, enemy_rect)
        else:
            # Fallback to red rectangle if no image
            pygame.draw.rect(self.game.screen, (255, 50, 50), enemy_rect)

        # Player frame in bottom left with image
        player_frame_rect = pygame.Rect(
            self.player_frame_pos[0],
            self.player_frame_pos[1],
            self.player_frame_size[0],
            self.player_frame_size[1],
        )
        pygame.draw.rect(self.game.screen, (100, 100, 100), player_frame_rect)
        
        # Draw player image in the frame
        player_image_rect = self.player_image.get_rect()
        player_image_rect.center = player_frame_rect.center
        self.game.screen.blit(self.player_image, player_image_rect)

        # Player HP bar and stats
        hp_percent = max(0, self.game.player.hp / 100)
        hp_width = int(self.player_frame_size[0] * hp_percent)
        hp_rect = pygame.Rect(
            self.player_frame_pos[0], self.player_frame_pos[1] - 45, hp_width, 15
        )
        pygame.draw.rect(self.game.screen, (0, 255, 0), hp_rect)

        hp_border_rect = pygame.Rect(
            self.player_frame_pos[0],
            self.player_frame_pos[1] - 45,
            self.player_frame_size[0],
            15,
        )
        pygame.draw.rect(self.game.screen, (255, 255, 255), hp_border_rect, 1)

        player_name = self.small_font.render(
            f"{self.game.player.name}",
            True,
            (255, 255, 255),
        )
        player_hp = self.small_font.render(
            f"HP: {self.game.player.hp}/100", True, (255, 255, 255)
        )
        player_atk = self.small_font.render(
            f"Damage: {self.game.player.atk}", True, (255, 255, 255)
        )

        text_x = self.player_frame_pos[0] + 5
        self.game.screen.blit(player_name, (text_x, self.player_frame_pos[1] - 65))
        self.game.screen.blit(player_hp, (text_x, self.player_frame_pos[1] - 45))
        self.game.screen.blit(player_atk, (text_x, self.player_frame_pos[1] - 20))

        # Enemy frame in bottom right with goblin image
        enemy_frame_rect = pygame.Rect(
            self.enemy_frame_pos[0],
            self.enemy_frame_pos[1],
            self.enemy_frame_size[0],
            self.enemy_frame_size[1],
        )
        pygame.draw.rect(self.game.screen, (100, 100, 100), enemy_frame_rect)
        
        # Draw enemy image in the frame
        if self.enemy_image:
            enemy_image_rect = self.enemy_image.get_rect()
            enemy_image_rect.center = enemy_frame_rect.center
            self.game.screen.blit(self.enemy_image, enemy_image_rect)
        else:
            # Fallback to red rectangle if no image
            pygame.draw.rect(
                self.game.screen, (255, 50, 50), enemy_frame_rect.inflate(-20, -20)
            )

        # Enemy HP bar and stats
        enemy_hp_percent = max(0, self.enemy.hp / 100)
        enemy_hp_width = int(self.enemy_frame_size[0] * enemy_hp_percent)
        enemy_hp_rect = pygame.Rect(
            self.enemy_frame_pos[0], self.enemy_frame_pos[1] - 45, enemy_hp_width, 15
        )
        pygame.draw.rect(self.game.screen, (0, 255, 0), enemy_hp_rect)

        enemy_hp_border_rect = pygame.Rect(
            self.enemy_frame_pos[0],
            self.enemy_frame_pos[1] - 45,
            self.enemy_frame_size[0],
            15,
        )
        pygame.draw.rect(self.game.screen, (255, 255, 255), enemy_hp_border_rect, 1)

        enemy_type = getattr(self.enemy, "enemy_type", "Enemy")
        enemy_name = self.small_font.render(f"{enemy_type}", True, (255, 255, 255))
        enemy_hp = self.small_font.render(
            f"HP: {self.enemy.hp}/100", True, (255, 255, 255)
        )
        enemy_atk = self.small_font.render(
            f"Damage: {self.enemy.damage}", True, (255, 255, 255)
        )

        enemy_text_x = self.enemy_frame_pos[0] + 5
        self.game.screen.blit(enemy_name, (enemy_text_x, self.enemy_frame_pos[1] - 65))
        self.game.screen.blit(enemy_hp, (enemy_text_x, self.enemy_frame_pos[1] - 45))
        self.game.screen.blit(enemy_atk, (enemy_text_x, self.enemy_frame_pos[1] - 20))

        action_box_rect = pygame.Rect(
            self.action_box_pos[0],
            self.action_box_pos[1],
            self.action_box_size[0],
            self.action_box_size[1],
        )
        pygame.draw.rect(self.game.screen, (50, 50, 50), action_box_rect)

        action_title = self.font.render("Battle Log", True, (255, 255, 0))
        self.game.screen.blit(
            action_title, (self.action_box_pos[0] + 10, self.action_box_pos[1] + 5)
        )

        visible_area_height = self.action_box_size[1] - 45 - self.log_margin_bottom
        max_visible_entries = min(self.visible_log_entries, len(self.battle_log))

        log_clip_area = pygame.Rect(
            self.action_box_pos[0] + 5,
            self.action_box_pos[1] + 35,
            self.action_box_size[0] - 10,
            visible_area_height,
        )

        old_clip = self.game.screen.get_clip()
        self.game.screen.set_clip(log_clip_area)

        for i in range(max_visible_entries):
            log_index = i + self.log_scroll_position
            if log_index < len(self.battle_log):
                log_entry = self.battle_log[log_index]
                log_text = self.small_font.render(log_entry, True, (255, 255, 255))
                self.game.screen.blit(
                    log_text,
                    (
                        self.action_box_pos[0] + 10,
                        self.action_box_pos[1] + 35 + i * 15,
                    ),
                )

        self.game.screen.set_clip(old_clip)

        attack_button_color = (200, 50, 50)
        if self.selected_button == 0:
            attack_button_color = (255, 80, 80)
            pygame.draw.rect(
                self.game.screen,
                (255, 255, 255),
                self.attack_button_rect.inflate(6, 6),
                2,
            )
        pygame.draw.rect(self.game.screen, attack_button_color, self.attack_button_rect)
        attack_text = self.font.render("Attack", True, (255, 255, 255))
        attack_text_rect = attack_text.get_rect(center=self.attack_button_rect.center)
        self.game.screen.blit(attack_text, attack_text_rect)

        skill_color = (
            (50, 100, 200) if self.game.player.skill_cooldown <= 0 else (100, 100, 100)
        )
        if self.selected_button == 1:
            skill_color = (
                (80, 130, 255)
                if self.game.player.skill_cooldown <= 0
                else (130, 130, 130)
            )
            pygame.draw.rect(
                self.game.screen,
                (255, 255, 255),
                self.skill_button_rect.inflate(6, 6),
                2,
            )
        pygame.draw.rect(self.game.screen, skill_color, self.skill_button_rect)

        if self.game.player.skill_cooldown > 0:
            skill_text = self.font.render(
                f"Skill ({self.game.player.skill_cooldown:.1f}s)", True, (255, 255, 255)
            )
        else:
            skill_text = self.font.render("Skill", True, (255, 255, 255))
        skill_text_rect = skill_text.get_rect(center=self.skill_button_rect.center)
        self.game.screen.blit(skill_text, skill_text_rect)

        ultimate_color = (
            (200, 150, 50)
            if self.game.player.ultimate_cooldown <= 0
            else (100, 100, 100)
        )
        if self.selected_button == 2:
            ultimate_color = (
                (255, 180, 80)
                if self.game.player.ultimate_cooldown <= 0
                else (130, 130, 130)
            )
            pygame.draw.rect(
                self.game.screen,
                (255, 255, 255),
                self.ultimate_button_rect.inflate(6, 6),
                2,
            )
        pygame.draw.rect(self.game.screen, ultimate_color, self.ultimate_button_rect)

        if self.game.player.ultimate_cooldown > 0:
            ultimate_text = self.font.render(
                f"Ultimate ({self.game.player.ultimate_cooldown:.1f}s)",
                True,
                (255, 255, 255),
            )
        else:
            ultimate_text = self.font.render("Ultimate", True, (255, 255, 255))
        ultimate_text_rect = ultimate_text.get_rect(
            center=self.ultimate_button_rect.center
        )
        self.game.screen.blit(ultimate_text, ultimate_text_rect)

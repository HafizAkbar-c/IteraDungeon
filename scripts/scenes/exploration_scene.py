import pygame
from scenes.base_scene import BaseScene
from attack import Attack
from floors import FirstFloor, SecondFloor, ThirdFloor
from scenes.story_transition_scene import StoryTransitionScene


class ExplorationScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.stop()
        self.exploration_music = pygame.mixer.Sound(
            "scripts/assets/audio/exploration.mp3"
        )
        self.exploration_music.set_volume(0.4)
        self.exploration_music.play(-1)
        self.player_speed = 5
        self.font = pygame.font.SysFont(None, 24)
        self.menu_active = False
        self.menu_options = ["Skill Tree", "Options", "Exit to Main Menu"]
        self.menu_selected = 0
        self.facing = "front"
        self.sword = Attack(self)
        self.is_attacking = False
        self.attack_timer = 0
        self.footstep_sound = pygame.mixer.Sound("scripts/assets/audio/Footstep.wav")
        self.footstep_cooldown = 0
        self.footstep_delay = 20
        self.floors = [FirstFloor(), SecondFloor(), ThirdFloor()]
        self.current_floor_index = 0
        self.current_floor = self.floors[self.current_floor_index]
        self.game.player.set_floor_abilities(self.current_floor_index)
        self.ground_color = (100, 70, 40)
        self.background_color = (135, 206, 235)
        self.first_floor_background = pygame.image.load(
            "scripts/assets/Background/first_floor_scene.png"
        )
        self.first_floor_background = pygame.transform.scale(
            self.first_floor_background,
            (self.game.screen.get_width(), self.game.screen.get_height()),
        )
        self.second_floor_background = pygame.image.load(
            "scripts/assets/Background/Floor 2/explore.png"
        )
        self.second_floor_background = pygame.transform.scale(
            self.second_floor_background,
            (self.game.screen.get_width(), self.game.screen.get_height()),
        )
        self.third_floor_background = pygame.image.load(
            "scripts/assets/Background/Floor 3/Explore bg.png"
        )
        self.third_floor_background = pygame.transform.scale(
            self.third_floor_background,
            (self.game.screen.get_width(), self.game.screen.get_height()),
        )
        self.generic_background = pygame.Surface(
            (self.game.screen.get_width(), self.game.screen.get_height())
        )
        self.generic_background.fill((30, 30, 40))

    def return_to_menu(self):
        from scenes.mainmenu_scene import MainMenuScene

        self.game.scene_manager.go_to(MainMenuScene(self.game))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.running = False
                elif event.key == pygame.K_x:
                    if not self.current_floor.cleared and self.check_enemy_collision():
                        self.is_attacking = True
                        self.attack_timer = 30
                        self.start_battle(self.current_floor.enemy)
                    else:
                        self.is_attacking = True
                        self.attack_timer = 30
                elif event.key == pygame.K_UP:
                    self.current_floor.jump()

    def update(self):
        keys = pygame.key.get_pressed()
        if not self.menu_active:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.current_floor.player_pos[0] -= self.player_speed
                self.game.player.facing = "left"
                self.facing = "left"
                if self.footstep_cooldown <= 0:
                    self.footstep_sound.play()
                    self.footstep_cooldown = self.footstep_delay
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.current_floor.player_pos[0] += self.player_speed
                self.game.player.facing = "right"
                self.facing = "right"
                if self.footstep_cooldown <= 0:
                    self.footstep_sound.play()
                    self.footstep_cooldown = self.footstep_delay
            else:
                if not self.is_attacking:
                    self.facing = "front"

            if self.is_attacking:
                self.attack_timer -= 1
                if self.attack_timer <= 0:
                    self.is_attacking = False

            self.current_floor.apply_gravity()

            if self.current_floor.check_reached_end():
                self.go_to_next_floor()

            if self.footstep_cooldown > 0:
                self.footstep_cooldown -= 1

    def go_to_next_floor(self):
        if self.current_floor_index < len(self.floors) - 1:
            next_floor_index = self.current_floor_index + 1
            next_floor = self.floors[next_floor_index]

            new_exploration_scene = ExplorationScene(self.game)
            new_exploration_scene.current_floor_index = next_floor_index
            new_exploration_scene.current_floor = new_exploration_scene.floors[
                next_floor_index
            ]
            new_exploration_scene.current_floor.player_pos[0] = 100
            self.game.player.set_floor_abilities(next_floor_index)

            story_scene = StoryTransitionScene(
                self.game,
                next_floor.story_text,
                new_exploration_scene,
                delay_per_line=3.0,
            )

            self.game.scene_manager.go_to(story_scene)
        else:
            print("Congratulations! You've completed all floors!")

    def check_enemy_collision(self):
        if self.current_floor.enemy in self.current_floor.defeated_enemies:
            return False

        player_rect = pygame.Rect(
            self.current_floor.player_pos[0],
            self.current_floor.player_pos[1] - 40,
            40,
            40,
        )

        enemy_proximity_rect = pygame.Rect(
            self.current_floor.enemy.rect.x - 20,
            self.current_floor.enemy.rect.y - 20,
            self.current_floor.enemy.rect.width + 40,
            self.current_floor.enemy.rect.height + 40,
        )

        return player_rect.colliderect(enemy_proximity_rect)

    def check_attack_hits_enemy(self):
        if not self.sword.active:
            return False
        hitbox = self.sword.get_hitbox()
        if self.current_floor.enemy not in self.current_floor.defeated_enemies:
            return self.current_floor.enemy.check_hit_by(hitbox)
        return False

    def render(self):
        if self.current_floor_index == 0:
            self.game.screen.blit(self.first_floor_background, (0, 0))
        elif self.current_floor_index == 1:
            self.game.screen.blit(self.second_floor_background, (0, 0))
        elif self.current_floor_index == 2:
            self.game.screen.blit(self.third_floor_background, (0, 0))
        else:
            self.game.screen.blit(self.generic_background, (0, 0))

        floor_text = self.font.render(
            f"{self.current_floor.name}", True, (255, 255, 255)
        )
        self.game.screen.blit(floor_text, (10, 10))

        if self.current_floor.cleared:
            next_text = self.font.render(
                "Go to the right to proceed to next floor", True, (255, 255, 0)
            )
            self.game.screen.blit(next_text, (self.game.screen.get_width() - 300, 10))

        if self.is_attacking:
            if self.facing == "left":
                image = pygame.transform.flip(
                    self.game.player.get_attack_frame(), True, False
                )
            else:
                image = self.game.player.get_attack_frame()
        elif self.facing == "right":
            image = self.game.player.get_walk_frame()
        elif self.facing == "left":
            image = pygame.transform.flip(
                self.game.player.get_walk_frame(), True, False
            )
        else:
            image = self.game.player.front_image

        self.game.screen.blit(
            image,
            (self.current_floor.player_pos[0], self.current_floor.player_pos[1] - 60),
        )

        if self.current_floor.enemy not in self.current_floor.defeated_enemies:
            self.current_floor.enemy.draw(self.game.screen)

    def start_battle(self, enemy):
        from scenes.battle_scene.battle_scene import BattleScene

        self.exploration_music.stop()

        self.current_floor.save_battle_position(self.current_floor.player_pos)
        self.current_floor.in_battle = True
        self.game.scene_manager.go_to(BattleScene(self.game, enemy, self))

    def on_battle_complete(self, enemy_defeated=False):
        if enemy_defeated:
            self.current_floor.defeat_enemy()
        self.current_floor.returning_from_battle = True
        self.current_floor.in_battle = False

        self.game.player.hp = 100

    def show_ending(self):
        ending_story = [
            "Naga yang mengerikan itu akhirnya jatuh ke tanah dengan dentuman keras.",
            "Kamu berdiri terengah-pernah, nyaris tidak percaya bahwa kamu berhasil mengalahkannya.",
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

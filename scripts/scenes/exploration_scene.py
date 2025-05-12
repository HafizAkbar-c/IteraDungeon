import pygame
from scenes.base_scene import BaseScene
from attack import Attack
from floors import FirstFloor, SecondFloor, ThirdFloor
from scenes.story_transition_scene import StoryTransitionScene


class ExplorationScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.player_speed = 5
        self.font = pygame.font.SysFont(None, 24)
        self.menu_active = False
        self.menu_options = ["Profile", "Skill Tree", "Options", "Exit to Main Menu"]
        self.menu_selected = 0
        self.facing = "right"
        self.sword = Attack(self)

        self.floors = [FirstFloor(), SecondFloor(), ThirdFloor()]
        self.current_floor_index = 0
        self.current_floor = self.floors[self.current_floor_index]

        # Set skill dan ultimate berdasarkan lantai saat ini
        self.game.player.set_floor_abilities(self.current_floor_index)

        self.ground_color = (100, 70, 40)
        self.background_color = (135, 206, 235)
        
        # Load background image for first floor
        self.first_floor_background = pygame.image.load("scripts/assets/Background/first_floor_scene.png")
        # Scale background to fit screen size
        self.first_floor_background = pygame.transform.scale(self.first_floor_background, (self.game.screen.get_width(), self.game.screen.get_height()))

    def return_to_menu(self):
        from scenes.mainmenu_scene import MainMenuScene

        self.game.scene_manager.go_to(MainMenuScene(self.game))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if self.menu_active:
                    if event.key == pygame.K_UP:
                        self.menu_selected = (self.menu_selected - 1) % len(
                            self.menu_options
                        )
                    elif event.key == pygame.K_DOWN:
                        self.menu_selected = (self.menu_selected + 1) % len(
                            self.menu_options
                        )
                    elif event.key == pygame.K_RETURN:
                        self.select_menu_option()
                    elif event.key == pygame.K_ESCAPE:
                        self.menu_active = False
                else:
                    if event.key == pygame.K_ESCAPE:
                        self.menu_active = True
                    elif event.key == pygame.K_z:
                        from scenes.skilltree_scene import SkillTreeScene

                        self.game.scene_manager.push(SkillTreeScene(self.game))
                    elif event.key == pygame.K_x:
                        if (
                            not self.current_floor.cleared
                            and self.check_enemy_collision()
                        ):
                            self.start_battle(
                                self.current_floor.enemy, player_first=True
                            )
                    elif event.key == pygame.K_UP:
                        self.current_floor.jump()

    def update(self):
        keys = pygame.key.get_pressed()
        if not self.menu_active:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.current_floor.player_pos[0] -= self.player_speed
                self.game.player.facing = "left"
                if self.current_floor.player_pos[0] < 20:
                    self.current_floor.player_pos[0] = 20

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.current_floor.player_pos[0] += self.player_speed
                self.game.player.facing = "right"
                if (
                    not self.current_floor.cleared
                    and self.current_floor.player_pos[0]
                    > self.game.screen.get_width() - 60
                ):
                    self.current_floor.player_pos[0] = self.game.screen.get_width() - 60

            self.current_floor.apply_gravity()

            if self.current_floor.check_reached_end():
                self.go_to_next_floor()

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
        # If we're on the first floor, use the first floor background image
        if self.current_floor_index == 0:
            self.game.screen.blit(self.first_floor_background, (0, 0))
        else:
            # Original background rendering for other floors
            self.game.screen.fill(self.background_color)
            
            ground_rect = pygame.Rect(
                0,
                self.current_floor.ground_level,
                self.game.screen.get_width(),
                self.game.screen.get_height() - self.current_floor.ground_level,
            )
            pygame.draw.rect(self.game.screen, self.ground_color, ground_rect)

        floor_text = self.font.render(
            f"{self.current_floor.name}", True, (255, 255, 255)
        )
        self.game.screen.blit(floor_text, (10, 10))

        if self.current_floor.cleared:
            next_text = self.font.render(
                "Go to the right to proceed to next floor", True, (255, 255, 0)
            )
            self.game.screen.blit(next_text, (self.game.screen.get_width() - 300, 10))

        player_color = (0, 200, 255)
        player_rect = pygame.Rect(
            self.current_floor.player_pos[0],
            self.current_floor.player_pos[1] - 40,
            40,
            40,
        )
        pygame.draw.rect(self.game.screen, player_color, player_rect)

        if self.menu_active:
            overlay = pygame.Surface((300, 300))
            overlay.set_alpha(200)
            overlay.fill((50, 50, 50))
            self.game.screen.blit(overlay, (250, 150))
            for idx, item in enumerate(self.menu_options):
                color = (255, 255, 0) if idx == self.menu_selected else (255, 255, 255)
                text = self.font.render(item, True, color)
                self.game.screen.blit(text, (270, 170 + idx * 30))

        if self.current_floor.enemy not in self.current_floor.defeated_enemies:
            self.current_floor.enemy.draw(self.game.screen)

    def handle_menu_selection(self):
        selected = self.menu_options[self.menu_selected]
        if selected == "Profile":
            from scenes.profile_scene import ProfileScene

            self.game.scene_manager.go_to(ProfileScene(self.game))
        elif selected == "Skill Tree":
            print("Open Skill Tree (Belum dibuat)")
        elif selected == "Options":
            print("Open Options (Belum dibuat)")
        elif selected == "Main Menu":
            from scenes.mainmenu_scene import MainMenuScene

            self.game.scene_manager.go_to(MainMenuScene(self.game))
        elif selected == "Exit Game":
            self.game.running = False

    def draw_menu(self):
        menu_surface = pygame.Surface((300, 200))
        menu_surface.fill((50, 50, 50))
        for idx, option in enumerate(self.menu_options):
            color = (255, 255, 0) if idx == self.menu_selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            menu_surface.blit(text, (20, 20 + idx * 40))
        self.game.screen.blit(
            menu_surface, (self.game.screen.get_width() // 2 - 150, 100)
        )

    def select_menu_option(self):
        option = self.menu_options[self.menu_selected]
        print(f"Selected: {option}")
        if option == "Profile":
            from scenes.profile_scene import ProfileScene

            self.game.scene_manager.push(ProfileScene(self.game))
        elif option == "Skill Tree":
            from scenes.skilltree_scene import SkillTreeScene

            self.game.scene_manager.go_to(SkillTreeScene(self.game))
        elif option == "Options":
            print("Buka options (belum dibuat)")
        elif option == "Exit to Main Menu":
            self.return_to_menu()

    def start_battle(self, enemy, player_first):
        from scenes.battle_scene import BattleScene

        self.current_floor.save_battle_position(self.current_floor.player_pos)
        self.current_floor.in_battle = True
        self.game.scene_manager.go_to(BattleScene(self.game, enemy, player_first, self))

    def on_battle_complete(self, enemy_defeated=False):
        if enemy_defeated:
            self.current_floor.defeat_enemy()
        self.current_floor.returning_from_battle = True
        self.current_floor.in_battle = False

        # Reset HP tapi jangan reset cooldown
        self.game.player.hp = 100

        # Jangan panggil set_floor_abilities() di sini karena akan membuat instance skill dan ultimate baru
        # yang akan mereset cooldown

import pygame
from scenes.base_scene import BaseScene
from scenes.battle_scene.battleaction_handler import BattleActionHandler
from scenes.battle_scene.battle_logger import BattleLogger
from scenes.battle_scene.ultimate_animation_manager import UltimateAnimationManager
from scenes.battle_scene.uirenderer import UIRenderer


class BattleScene(BaseScene):
    def __init__(self, game, enemy, exploration_scene=None):
        super().__init__(game)
        # Stop any currently playing sound
        pygame.mixer.stop()

        self.enemy = enemy
        self.exploration_scene = exploration_scene
        self.current_floor_index = (
            0 if not exploration_scene else exploration_scene.current_floor_index
        )
        self.done = False

        self.punch_sound = pygame.mixer.Sound("scripts/assets/audio/Punch.wav")

        # Add sound effects for goblin, orc, and dragon battles
        if hasattr(self.enemy, "enemy_type"):
            if self.enemy.enemy_type == "Goblin":
                self.goblin_sound = pygame.mixer.Sound(
                    "scripts/assets/audio/goblin.mp3"
                )
                self.goblin_sound.set_volume(0.3)
                self.goblin_sound.play(-1)
            elif self.enemy.enemy_type == "Orc":
                self.orc_sound = pygame.mixer.Sound("scripts/assets/audio/orc.mp3")
                self.orc_sound.set_volume(0.3)
                self.orc_sound.play(-1)
            elif self.enemy.enemy_type == "Dragon":
                self.dragon_sound = pygame.mixer.Sound(
                    "scripts/assets/audio/dragon.mp3"
                )
                self.dragon_sound.set_volume(0.3)
                self.dragon_sound.play(-1)

        self.player_image = pygame.image.load(
            "scripts/assets/Background/Floor 1 battle/border1_00000.png"
        )
        self.player_image = pygame.transform.scale(self.player_image, (150, 150))

        self.background_image = pygame.image.load(
            "scripts/assets/Background/Floor 1 battle/Comp 1_00000.png"
        )
        self.background_image = pygame.transform.scale(
            self.background_image,
            (self.game.screen.get_width(), self.game.screen.get_height()),
        )

        self.border_player = pygame.image.load(
            "scripts/assets/Background/Floor 1 battle/border1_00000.png"
        )
        self.border_player = pygame.transform.scale(self.border_player, (300, 150))

        self.border_enemy = pygame.image.load(
            "scripts/assets/Background/Floor 1 battle/border2_00000.png"
        )
        self.border_enemy = pygame.transform.scale(self.border_enemy, (300, 150))

        self.center_goblin_idle = pygame.image.load(
            "scripts/assets/Background/Floor 1 battle/goblin_00002.png"
        )
        self.center_goblin_boss = pygame.image.load(
            "scripts/assets/Background/Floor 1 battle/goblin2_00002.png"
        )

        self.center_goblin_idle = pygame.transform.scale(
            self.center_goblin_idle, (200, 200)
        )
        self.center_goblin_boss = pygame.transform.scale(
            self.center_goblin_boss, (200, 200)
        )

        self.enemy_image = None
        self.center_enemy_image = None
        self._load_enemy_images()

        if exploration_scene and exploration_scene.current_floor_index is not None:
            if (
                self.game.player.current_skill is None
                or self.game.player.current_ultimate is None
            ):
                self.game.player.set_floor_abilities(
                    exploration_scene.current_floor_index
                )

        screen_width = game.screen.get_width()
        screen_height = game.screen.get_height()

        self.logger = BattleLogger(screen_width, screen_height)
        self.ui_renderer = UIRenderer(screen_width, screen_height)
        self.action_handler = BattleActionHandler(
            game.player, enemy, exploration_scene, self.logger, self.punch_sound
        )
        self.animation_manager = UltimateAnimationManager(screen_width, screen_height)

    def _load_enemy_images(self):
        if hasattr(self.enemy, "enemy_type"):
            if self.enemy.enemy_type == "Goblin":
                self.enemy_image = pygame.image.load(
                    "scripts/assets/Background/Floor 1 battle/border2_00000.png"
                )
                self.enemy_image = pygame.transform.scale(self.enemy_image, (150, 150))

                goblin_frame1 = pygame.image.load(
                    "scripts/assets/Background/Floor 1 battle/goblin_00002.png"
                )
                goblin_frame2 = pygame.image.load(
                    "scripts/assets/Background/Floor 1 battle/goblin2_00002.png"
                )

                goblin_frame1 = pygame.transform.scale(goblin_frame1, (500, 500))
                goblin_frame2 = pygame.transform.scale(goblin_frame2, (500, 500))

                self.center_enemy_frames = [goblin_frame1, goblin_frame2]
                self.current_enemy_frame = 0
                self.enemy_frame_timer = 0
                self.enemy_frame_interval = 1000

            elif self.enemy.enemy_type == "Orc":
                self.enemy_image = pygame.image.load(
                    "scripts/assets/Background/Floor 2/ogre border_00000.png"
                )
                self.enemy_image = pygame.transform.scale(self.enemy_image, (150, 150))

                orc_frame1 = pygame.image.load(
                    "scripts/assets/Background/Floor 2/per-frame ogre_00000.png"
                )
                orc_frame2 = pygame.image.load(
                    "scripts/assets/Background/Floor 2/per-frame ogre v2_00000.png"
                )

                orc_frame1 = pygame.transform.scale(orc_frame1, (500, 500))
                orc_frame2 = pygame.transform.scale(orc_frame2, (500, 500))

                self.center_enemy_frames = [orc_frame1, orc_frame2]
                self.current_enemy_frame = 0
                self.enemy_frame_timer = 0
                self.enemy_frame_interval = 1000

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.quit()
            elif event.type == pygame.KEYDOWN:
                if self.action_handler.turn == "player":
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if self.ui_renderer.selected_button == 0:
                            self.action_handler.use_attack()
                        elif self.ui_renderer.selected_button == 1:
                            self.action_handler.use_skill()
                        elif self.ui_renderer.selected_button == 2:
                            damage, frame_paths = self.action_handler.use_ultimate()
                            if damage > 0 and frame_paths:
                                duration = (
                                    self.game.player.current_ultimate.animation_duration
                                )
                                self.animation_manager.start_ultimate_animation(
                                    frame_paths, damage, duration
                                )
                    elif event.key == pygame.K_LEFT:
                        self.ui_renderer.selected_button = max(
                            0, self.ui_renderer.selected_button - 1
                        )
                    elif event.key == pygame.K_RIGHT:
                        self.ui_renderer.selected_button = min(
                            2, self.ui_renderer.selected_button + 1
                        )
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event)

    def _handle_mouse_click(self, event):
        if event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.action_handler.turn == "player":
                if self.ui_renderer.attack_button_rect.collidepoint(mouse_pos):
                    self.ui_renderer.selected_button = 0
                    self.action_handler.use_attack()
                elif (
                    self.ui_renderer.skill_button_rect.collidepoint(mouse_pos)
                    and self.game.player.skill_cooldown <= 0
                ):
                    # Only allow skill button click if not on cooldown
                    self.ui_renderer.selected_button = 1
                    self.action_handler.use_skill()
                elif (
                    self.ui_renderer.ultimate_button_rect.collidepoint(mouse_pos)
                    and self.game.player.ultimate_cooldown <= 0
                ):
                    # Only allow ultimate button click if not on cooldown
                    self.ui_renderer.selected_button = 2
                    damage, frame_paths = self.action_handler.use_ultimate()
                    if damage > 0 and frame_paths:
                        duration = self.game.player.current_ultimate.animation_duration
                        self.animation_manager.start_ultimate_animation(
                            frame_paths, damage, duration
                        )

    def update(self):
        self.game.player.update()

        animation_complete, damage = self.animation_manager.update()
        if animation_complete:
            self.action_handler.process_ultimate_damage(damage)

        if self.done:
            return

        self.enemy_frame_timer += self.game.clock.get_time()
        if self.enemy_frame_timer >= self.enemy_frame_interval:
            self.enemy_frame_timer = 0
            self.current_enemy_frame = (self.current_enemy_frame + 1) % len(
                self.center_enemy_frames
            )

        self._check_battle_outcome()

    def _check_battle_outcome(self):
        if self.enemy.hp <= 0:
            self.logger.add_to_battle_log("Kamu menang!")
            self.done = True

            if self.exploration_scene:
                if self.exploration_scene.current_floor:
                    self.exploration_scene.current_floor.set_turn(
                        self.action_handler.turn
                    )

                if self.exploration_scene.current_floor_index == 2:
                    self.exploration_scene.show_ending()
                else:
                    self.exploration_scene.on_battle_complete(enemy_defeated=True)
                    self.game.scene_manager.go_to(self.exploration_scene)
            else:
                from scenes.exploration_scene import ExplorationScene

                self.game.scene_manager.go_to(ExplorationScene(self.game))

        elif self.game.player.hp <= 0:
            self.logger.add_to_battle_log("Kamu kalah! Game over.")
            self.done = True
            self.game.quit()

    def render(self):
        if self.animation_manager.render(self.game.screen):
            return

        self.game.screen.blit(self.background_image, (0, 0))

        if hasattr(self, "center_enemy_frames"):
            current_center_image = self.center_enemy_frames[self.current_enemy_frame]
        else:
            current_center_image = self.center_enemy_image

        self.ui_renderer.render_enemy(
            self.game.screen, self.enemy, self.enemy_image, current_center_image
        )

        self.ui_renderer.render_player(
            self.game.screen, self.game.player, self.player_image
        )

        self.logger.render(self.game.screen)
        self.ui_renderer.render_buttons(self.game.screen, self.game.player)

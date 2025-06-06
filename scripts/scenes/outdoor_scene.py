import pygame
from scenes.base_scene import BaseScene
from scenes.story_transition_scene import StoryTransitionScene
from scenes.exploration_scene import ExplorationScene
from utils.font_helper import FontHelper


class OutdoorScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        pygame.mixer.stop()
        self.font = FontHelper.getFont("Minecraft", 24)
        self.player_pos = [100, 450]
        self.player_speed = 5
        self.entrance_pos = [700, 440]
        self.entrance_size = [80, 60]
        self.entrance_message_visible = False
        self.facing = "front"
        self.footstep_sound = pygame.mixer.Sound("scripts/assets/audio/Footstep.wav")
        self.footstep_cooldown = 0
        self.footstep_delay = 20
        self.background = pygame.image.load(
            "scripts/assets/Background/outdoor_scene.png"
        )
        self.background = pygame.transform.scale(
            self.background,
            (self.game.screen.get_width(), self.game.screen.get_height()),
        )
        self.outdoor_music = pygame.mixer.Sound("scripts/assets/audio/exploration.mp3")
        self.outdoor_music.set_volume(0.4)
        self.outdoor_music.play(-1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    from scenes.mainmenu_scene import MainMenuScene

                    self.game.scene_manager.go_to(MainMenuScene(self.game))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_pos[0] -= self.player_speed
            self.facing = "left"
            if self.footstep_cooldown <= 0:
                self.footstep_sound.play()
                self.footstep_cooldown = self.footstep_delay
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_pos[0] += self.player_speed
            self.facing = "right"
            if self.footstep_cooldown <= 0:
                self.footstep_sound.play()
                self.footstep_cooldown = self.footstep_delay
        else:
            self.facing = "front"

        if self.footstep_cooldown > 0:
            self.footstep_cooldown -= 1

        player_rect = pygame.Rect(
            self.player_pos[0],
            self.player_pos[1] - 60,
            self.game.player.player_size[0],
            self.game.player.player_size[1],
        )
        entrance_rect = pygame.Rect(
            self.entrance_pos[0],
            self.entrance_pos[1],
            self.entrance_size[0],
            self.entrance_size[1],
        )

        self.entrance_message_visible = player_rect.colliderect(entrance_rect)
        if self.entrance_message_visible and keys[pygame.K_RETURN]:
            self.enter_dungeon()

    def enter_dungeon(self):
        self.outdoor_music.stop()

        intro_story = [
            "Kamu telah menemukan pintu masuk menuju ke bawah tanah yang misterius...",
            "Dengan rasa penasaran, kamu melangkah masuk ke dalam kegelapan.",
            "Tiba-tiba, pintu di belakangmu tertutup dengan keras!",
            "Saat tersadar, kamu menemukan dirinya terjebak dalam Dungeon ITERA.",
            "Kamu harus menemukan jalan keluar dengan mengalahkan semua monster di tiap lantai.",
        ]
        exploration_scene = ExplorationScene(self.game)
        transition_scene = StoryTransitionScene(
            self.game, intro_story, exploration_scene, delay_per_line=2.5
        )
        self.game.scene_manager.go_to(transition_scene)

    def render(self):
        self.game.screen.blit(self.background, (0, 0))

        keys = pygame.key.get_pressed()
        moving = (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
            or keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
        )

        if self.facing == "right":
            if moving:
                image = self.game.player.get_walk_frame()
            else:
                image = self.game.player.walk_right_images[0]
        elif self.facing == "left":
            if moving:
                image = pygame.transform.flip(
                    self.game.player.get_walk_frame(), True, False
                )
            else:
                image = pygame.transform.flip(
                    self.game.player.walk_right_images[0], True, False
                )
        else:
            image = self.game.player.front_image

        self.game.screen.blit(image, (self.player_pos[0], self.player_pos[1] - 60))

        if self.entrance_message_visible:
            hint_text = self.font.render(
                "Tekan ENTER untuk masuk ke dungeon", True, (255, 255, 255)
            )
            text_rect = hint_text.get_rect(
                center=(self.game.screen.get_width() // 2, 100)
            )
            self.game.screen.blit(hint_text, text_rect)

import pygame
from scenes.base_scene import BaseScene
from scenes.story_transition_scene import StoryTransitionScene
from scenes.exploration_scene import ExplorationScene


class OutdoorScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 24)
        self.player_pos = [100, 400]
        self.player_speed = 5
        self.player_size = 40
        self.sky_color = (135, 206, 235)
        self.ground_color = (139, 69, 19)
        self.entrance_pos = [700, 390]
        self.entrance_size = [80, 60]
        self.entrance_message_visible = False

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
            if self.player_pos[0] < 20:
                self.player_pos[0] = 20
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_pos[0] += self.player_speed
            if self.player_pos[0] > self.game.screen.get_width() - 60:
                self.player_pos[0] = self.game.screen.get_width() - 60
        player_rect = pygame.Rect(
            self.player_pos[0],
            self.player_pos[1] - 40,
            self.player_size,
            self.player_size,
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
        self.game.screen.fill(self.sky_color)
        ground_rect = pygame.Rect(0, 400, self.game.screen.get_width(), 200)
        pygame.draw.rect(self.game.screen, self.ground_color, ground_rect)
        entrance_rect = pygame.Rect(
            self.entrance_pos[0],
            self.entrance_pos[1] - 30,
            self.entrance_size[0],
            self.entrance_size[1],
        )
        pygame.draw.rect(self.game.screen, (50, 50, 50), entrance_rect)
        player_color = (0, 200, 255)
        player_rect = pygame.Rect(
            self.player_pos[0],
            self.player_pos[1] - 40,
            self.player_size,
            self.player_size,
        )
        pygame.draw.rect(self.game.screen, player_color, player_rect)
        if self.entrance_message_visible:
            hint_text = self.font.render(
                "Tekan ENTER untuk masuk ke dungeon", True, (255, 255, 255)
            )
            text_rect = hint_text.get_rect(
                center=(self.game.screen.get_width() // 2, 100)
            )
            self.game.screen.blit(hint_text, text_rect)

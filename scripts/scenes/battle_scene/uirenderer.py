import pygame


class UIRenderer:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 20)

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

        self.center_enemy_size = (200, 200)

        self.button_width = 110
        self.button_height = 50
        self.button_margin = 25
        self.button_y = self.screen_height - 70

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

        self.selected_button = 0

    def render_player(self, screen, player, player_image):
        player_frame_rect = pygame.Rect(
            self.player_frame_pos[0],
            self.player_frame_pos[1],
            self.player_frame_size[0],
            self.player_frame_size[1],
        )
        pygame.draw.rect(screen, (100, 100, 100), player_frame_rect)

        player_image_rect = player_image.get_rect()
        player_image_rect.center = player_frame_rect.center
        screen.blit(player_image, player_image_rect)

        hp_percent = max(0, player.hp / 100)
        hp_width = int(self.player_frame_size[0] * hp_percent)
        hp_rect = pygame.Rect(
            self.player_frame_pos[0], self.player_frame_pos[1] - 45, hp_width, 15
        )
        pygame.draw.rect(screen, (0, 255, 0), hp_rect)

        hp_border_rect = pygame.Rect(
            self.player_frame_pos[0],
            self.player_frame_pos[1] - 45,
            self.player_frame_size[0],
            15,
        )
        pygame.draw.rect(screen, (255, 255, 255), hp_border_rect, 1)

        player_name = self.small_font.render(f"{player.name}", True, (255, 255, 255))
        player_hp = self.small_font.render(
            f"HP: {player.hp}/100", True, (255, 255, 255)
        )
        player_atk = self.small_font.render(
            f"Damage: {player.atk}", True, (255, 255, 255)
        )

        text_x = self.player_frame_pos[0] + 5
        screen.blit(player_name, (text_x, self.player_frame_pos[1] - 65))
        screen.blit(player_hp, (text_x, self.player_frame_pos[1] - 45))
        screen.blit(player_atk, (text_x, self.player_frame_pos[1] - 20))

    def render_enemy(self, screen, enemy, enemy_image, center_enemy_image):
        enemy_center_pos = (self.screen_width // 2, self.screen_height // 3)
        enemy_size = self.center_enemy_size
        enemy_rect = pygame.Rect(
            enemy_center_pos[0] - enemy_size[0] // 2,
            enemy_center_pos[1] - enemy_size[1] // 2,
            enemy_size[0],
            enemy_size[1],
        )

        if center_enemy_image:
            screen.blit(center_enemy_image, enemy_rect)
        else:
            pygame.draw.rect(screen, (255, 50, 50), enemy_rect)

        enemy_frame_rect = pygame.Rect(
            self.enemy_frame_pos[0],
            self.enemy_frame_pos[1],
            self.enemy_frame_size[0],
            self.enemy_frame_size[1],
        )
        pygame.draw.rect(screen, (100, 100, 100), enemy_frame_rect)

        if enemy_image:
            enemy_image_rect = enemy_image.get_rect()
            enemy_image_rect.center = enemy_frame_rect.center
            screen.blit(enemy_image, enemy_image_rect)
        else:
            pygame.draw.rect(screen, (255, 50, 50), enemy_frame_rect.inflate(-20, -20))

        enemy_hp_percent = max(0, enemy.hp / 100)
        enemy_hp_width = int(self.enemy_frame_size[0] * enemy_hp_percent)
        enemy_hp_rect = pygame.Rect(
            self.enemy_frame_pos[0], self.enemy_frame_pos[1] - 45, enemy_hp_width, 15
        )
        pygame.draw.rect(screen, (0, 255, 0), enemy_hp_rect)

        enemy_hp_border_rect = pygame.Rect(
            self.enemy_frame_pos[0],
            self.enemy_frame_pos[1] - 45,
            self.enemy_frame_size[0],
            15,
        )
        pygame.draw.rect(screen, (255, 255, 255), enemy_hp_border_rect, 1)

        enemy_type = getattr(enemy, "enemy_type", "Enemy")
        enemy_name = self.small_font.render(f"{enemy_type}", True, (255, 255, 255))
        enemy_hp = self.small_font.render(f"HP: {enemy.hp}/100", True, (255, 255, 255))
        enemy_atk = self.small_font.render(
            f"Damage: {enemy.damage}", True, (255, 255, 255)
        )

        enemy_text_x = self.enemy_frame_pos[0] + 5
        screen.blit(enemy_name, (enemy_text_x, self.enemy_frame_pos[1] - 65))
        screen.blit(enemy_hp, (enemy_text_x, self.enemy_frame_pos[1] - 45))
        screen.blit(enemy_atk, (enemy_text_x, self.enemy_frame_pos[1] - 20))

    def render_buttons(self, screen, player):
        attack_button_color = (200, 50, 50)
        if self.selected_button == 0:
            attack_button_color = (255, 80, 80)
            pygame.draw.rect(
                screen, (255, 255, 255), self.attack_button_rect.inflate(6, 6), 2
            )
        pygame.draw.rect(screen, attack_button_color, self.attack_button_rect)
        attack_text = self.font.render("Attack", True, (255, 255, 255))
        attack_text_rect = attack_text.get_rect(center=self.attack_button_rect.center)
        screen.blit(attack_text, attack_text_rect)

        skill_color = (50, 100, 200) if player.skill_cooldown <= 0 else (100, 100, 100)
        if self.selected_button == 1:
            skill_color = (
                (80, 130, 255) if player.skill_cooldown <= 0 else (130, 130, 130)
            )
            pygame.draw.rect(
                screen, (255, 255, 255), self.skill_button_rect.inflate(6, 6), 2
            )
        pygame.draw.rect(screen, skill_color, self.skill_button_rect)

        if player.skill_cooldown > 0:
            skill_text = self.font.render(
                f"Skill ({player.skill_cooldown:.1f}s)", True, (255, 255, 255)
            )
        else:
            skill_text = self.font.render("Skill", True, (255, 255, 255))
        skill_text_rect = skill_text.get_rect(center=self.skill_button_rect.center)
        screen.blit(skill_text, skill_text_rect)

        ultimate_color = (
            (200, 150, 50) if player.ultimate_cooldown <= 0 else (100, 100, 100)
        )
        if self.selected_button == 2:
            ultimate_color = (
                (255, 180, 80) if player.ultimate_cooldown <= 0 else (130, 130, 130)
            )
            pygame.draw.rect(
                screen, (255, 255, 255), self.ultimate_button_rect.inflate(6, 6), 2
            )
        pygame.draw.rect(screen, ultimate_color, self.ultimate_button_rect)

        if player.ultimate_cooldown > 0:
            ultimate_text = self.font.render(
                f"Ultimate ({player.ultimate_cooldown:.1f}s)", True, (255, 255, 255)
            )
        else:
            ultimate_text = self.font.render("Ultimate", True, (255, 255, 255))
        ultimate_text_rect = ultimate_text.get_rect(
            center=self.ultimate_button_rect.center
        )
        screen.blit(ultimate_text, ultimate_text_rect)

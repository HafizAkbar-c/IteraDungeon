import pygame

class BattleLogger:
    def __init__(self, screen_width, screen_height):
        self.battle_log = ["Pertempuran dimulai!"]
        self.max_log_entries = 8
        self.visible_log_entries = min(6, self.max_log_entries)
        self.log_scroll_position = 0

        self.font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 20)

        self.action_box_size = (300, 150)
        self.action_box_pos = (screen_width - 330, 20)
        self.log_margin_bottom = 15

    def add_to_battle_log(self, message):
        self.battle_log.append(message)
        if len(self.battle_log) > self.max_log_entries:
            self.battle_log.pop(0)

        if len(self.battle_log) > self.visible_log_entries:
            self.log_scroll_position = len(self.battle_log) - self.visible_log_entries

    def render(self, screen):
        action_box_rect = pygame.Rect(
            self.action_box_pos[0],
            self.action_box_pos[1],
            self.action_box_size[0],
            self.action_box_size[1],
        )
        pygame.draw.rect(screen, (50, 50, 50), action_box_rect)

        action_title = self.font.render("Battle Log", True, (255, 255, 0))
        screen.blit(
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

        old_clip = screen.get_clip()
        screen.set_clip(log_clip_area)

        for i in range(max_visible_entries):
            log_index = i + self.log_scroll_position
            if log_index < len(self.battle_log):
                log_entry = self.battle_log[log_index]
                log_text = self.small_font.render(log_entry, True, (255, 255, 255))
                screen.blit(
                    log_text,
                    (
                        self.action_box_pos[0] + 10,
                        self.action_box_pos[1] + 35 + i * 15,
                    ),
                )

        screen.set_clip(old_clip)

from enemy import Enemy, Goblin, Orc, Dragon


class Floor:
    def __init__(self, name, enemy_type, story_text, enemy_x=500, enemy_y=450):
        self.name = name
        self.enemy_type = enemy_type
        self.story_text = story_text
        self.cleared = False
        self.player_pos = [100, 450]
        self.last_position_before_battle = [100, 450]
        self.enemy = Enemy(enemy_x, enemy_y)
        self.defeated_enemies = set()
        self.returning_from_battle = False
        self.in_battle = False
        self.current_turn = "player"
        self.ground_level = 450
        self.player_velocity_y = 0
        self.player_jumping = False
        self.gravity = 0.5
        self.screen_width = 800

    def defeat_enemy(self):
        if not self.cleared:
            print(f"You have defeated the enemy: {self.enemy_type} on {self.name}!")
            self.cleared = True
            self.defeated_enemies.add(self.enemy)
        else:
            print(f"The {self.name} is already cleared.")

    def is_cleared(self):
        return self.cleared

    def save_player_position(self, position):
        self.player_pos = position.copy()

    def save_battle_position(self, position):
        self.last_position_before_battle = position.copy()

    def check_reached_end(self):
        if not self.cleared:
            return False
        return self.player_pos[0] > self.screen_width - 50

    def apply_gravity(self):
        if self.player_pos[1] < self.ground_level or self.player_velocity_y != 0:
            self.player_velocity_y += self.gravity
            self.player_pos[1] += self.player_velocity_y

            if self.player_pos[1] >= self.ground_level:
                self.player_pos[1] = self.ground_level
                self.player_velocity_y = 0
                self.player_jumping = False

    def jump(self):
        if not self.player_jumping and self.player_pos[1] >= self.ground_level:
            self.player_velocity_y = -12
            self.player_jumping = True

    def set_turn(self, turn):
        self.current_turn = turn

    def get_battle_stats(self):
        return {
            "enemy_hp": self.enemy.hp,
            "turn": self.current_turn,
            "cleared": self.cleared,
        }


class FirstFloor(Floor):
    def __init__(self):
        story_text = [
            "Kamu terbangun di dalam ruangan bawah tanah yang gelap.",
            "Kamu tidak ingat bagaimana kamu bisa sampai di sini.",
            "Hanya ada satu jalan keluar, yaitu maju ke depan.",
            "Dalam kegelapan, kamu melihat sosok yang mengintai...",
        ]
        super().__init__("First Floor", "Goblin", story_text, 500, 450)
        self.enemy = Goblin(500, 590)


class SecondFloor(Floor):
    def __init__(self):
        story_text = [
            "Setelah mengalahkan musuh pertama, kamu melanjutkan perjalanan.",
            "Koridor semakin gelap dan lembab.",
            "Suara-suara aneh terdengar dari kejauhan.",
            "Sesuatu yang lebih kuat menunggumu di depan.",
        ]
        super().__init__("Second Floor", "Orc", story_text, 500, 450)
        self.enemy = Orc(500, 590)


class ThirdFloor(Floor):
    def __init__(self):
        story_text = [
            "Kamu telah tiba di lantai terakhir.",
            "Udara terasa panas dan berat.",
            "Asap dan aura kematian menyelimuti sekitarmu.",
            "Dari kejauhan, kamu melihat siluet naga yang sedang tertidur...",
        ]
        super().__init__("Third Floor", "Dragon", story_text, 500, 450)
        self.enemy = Dragon(500, 450)

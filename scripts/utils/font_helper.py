import os
import pygame


class FontHelper:
    @staticmethod
    def getFont(font_name, font_size=24):
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        font_path = os.path.join(script_dir, "assets", "fonts", f"{font_name}.ttf")
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font file {font_path} not found.")
        return pygame.font.Font(font_path, font_size)

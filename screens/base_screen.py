from abc import ABC

import pygame


class BaseScreen(ABC):
    def __init__(self):
        font_path = "assets/fonts/PressStart2P-Regular.ttf"
        self.title_font = pygame.font.Font(font_path, 32)
        self.font_text = pygame.font.Font(font_path, 16)
        self.font_big = pygame.font.Font(None, 96)
        self.font_small = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 45)
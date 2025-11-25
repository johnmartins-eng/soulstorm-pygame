import pygame

import config
from ui.hud import HUD
from utils.camera import Camera


class GameContext:
    def __init__(self):
        # Initialize Groups
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.attacks = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.orbitals = pygame.sprite.Group()
        self.player = None
        self.camera: Camera = Camera(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        # inform camera about total world size so it can clamp properly
        try:
            self.camera.set_world_size(config.WORLD_WIDTH, config.WORLD_HEIGHT)
        except Exception:
            pass
        self.hud: HUD = HUD(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

    def reset(self):
        self.all_sprites.empty()
        self.enemies.empty()
        self.attacks.empty()
        self.items.empty()
        self.orbitals.empty()
        self.player = None
        self.camera: Camera = Camera(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        try:
            self.camera.set_world_size(config.WORLD_WIDTH, config.WORLD_HEIGHT)
        except Exception:
            pass
        self.hud: HUD = HUD(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

    def add_player(self, sprite):
        self.player = sprite
        self.all_sprites.add(sprite)

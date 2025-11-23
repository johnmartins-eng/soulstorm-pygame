import pygame
from abc import ABC, abstractmethod

from entities.base_entity import BaseEntity
from entities.enemies.base_enemy import BaseEnemy
from entities.player import Player
from utils.direction_enum import DirectionEnum


class BaseOrbital(pygame.sprite.Sprite, ABC):
    def __init__(self, player: Player, speed: float, base_damage: float):
        super().__init__()
        self.player = player
        self.speed = speed
        self.base_damage = base_damage
        self.direction = player.direction

        self.frames: list[pygame.Surface] = []
        self.image: pygame.Surface | None = None
        self.rect: pygame.Rect | None = None

        self.frame_count: float = 0
        self.active_frame: int = 0

        self.load_frames()

        self.damage_done = False

        if self.frames:
            self.image = self.frames[0]
            self.rect = self.image.get_rect(topleft=(self.player.rect.x, self.player.rect.y))
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 255))
            self.rect = self.image.get_rect(topleft=(self.player.rect.x, self.player.rect.y))

    
    def on_hit(self, target: BaseEntity):
        if isinstance(target, BaseEnemy):
            target.take_damage(self.base_damage)

    @abstractmethod
    def load_frames(self):
        raise NotImplementedError

    @abstractmethod
    def update_animation(self):
        raise NotImplementedError
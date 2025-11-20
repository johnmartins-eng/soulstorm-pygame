import pygame
from abc import ABC, abstractmethod

from entities.base_entity import BaseEntity
from entities.enemies.base_enemy import BaseEnemy

class BaseAttack(pygame.sprite.Sprite, ABC):
    def __init__(self, player, speed: float):
        super().__init__()
        self.player = player
        self.x = player.rect.x
        self.y = player.rect.y

        self.speed = speed
        self.base_damage = player.base_damage
        self.direction = player.direction
        self.facing_right = player.facing_right

        self.frames: list[pygame.Surface] = []
        self.image: pygame.Surface | None = None
        self.rect: pygame.Rect | None = None

        self.frame_count: float = 0
        self.active_frame: int = 0

        self.load_frames()

        if self.frames:
            self.image = self.frames[0]
            self.rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 255))
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

    
    def on_hit(self, target: BaseEntity):
        if isinstance(target, BaseEnemy):
            target.take_damage(self.base_damage)

    @abstractmethod
    def load_frames(self):
        raise NotImplementedError

    @abstractmethod
    def update_animation(self):
        raise NotImplementedError
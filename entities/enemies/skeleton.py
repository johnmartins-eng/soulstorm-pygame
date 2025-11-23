import math
import pygame
from entities.base_entity import AnimationModeEnum
from entities.enemies.base_enemy import BaseEnemy
from entities.items.jewel import Jewel


class Skeleton(BaseEnemy):
    def __init__(self, x=100, y=50, health=100, base_damage=5, speed=1.5):
        super().__init__(x, y, health, base_damage, speed)
        self.animation_mode = AnimationModeEnum.RUNNING
        # xp value on death
        self.xp_value = 10

    def load_frames(self):
        # running frames
        for i in range(0, 12):
            name = f"sprite_0{i}.png" if i < 10 else f"sprite_{i}.png"
            img = pygame.image.load(
                f"assets/enemies/skeleton/walking/{name}").convert_alpha()
            self.frames.append(pygame.transform.scale(img, (50, 70)))

        # dying frames
        for i in range(0, 15):
            name = f"sprite_0{i}.png" if i < 10 else f"sprite_{i}.png"
            img = pygame.image.load(
                f"assets/enemies/skeleton/dying/{name}").convert_alpha()
            self.frames.append(pygame.transform.scale(img, (50, 70)))


    def update_animation(self):
        if self.frame_count >= 60:
            self.frame_count = 0

        if self.animation_mode == AnimationModeEnum.RUNNING:
            frame_intervals = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60]
            frame_indexes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

        if self.animation_mode == AnimationModeEnum.DYING:
            frame_intervals = [4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60]
            frame_indexes = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]

        for i in range(len(frame_intervals) - 1):
            if frame_intervals[i] <= self.frame_count < frame_intervals[i + 1]:
                self.active_frame = frame_indexes[i]
                break

        self.frame_count += 1
        self.image = self.frames[self.active_frame]

        # Flip image based on facing direction
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)
        

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0 and self.dying is False:
            self.animation_mode = AnimationModeEnum.DYING
            self.frame_count = 0
            self.dying = True
            

    def attack(self, target):
        target.take_damage(self.base_damage)

    def go_to_player(self, target: pygame.sprite.Sprite):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = target.rect.x - self.rect.x, target.rect.y - self.rect.y
        dist = math.hypot(dx, dy)
        if dist <= 0:
            self.attack(target)
            return
        dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed
        # Update facing direction
        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False

    def update(self, target: pygame.sprite.Sprite, items_group: pygame.sprite.Group = None, all_sprites_group: pygame.sprite.Group =None, *args, **kwargs):
        if self.dying:
            self.update_animation()
            if self.frame_count >= 60:
                j = Jewel(self.rect.x, self.rect.y)
                self.items_group.add(j)
                self.all_sprites_group.add(j)
                self.kill()
            return
            
        self.update_animation()
        self.items_group = items_group
        self.all_sprites_group = all_sprites_group
        if target is not None:
            self.go_to_player(target)

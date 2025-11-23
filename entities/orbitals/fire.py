import math
import pygame
from entities.orbitals.base_orbital import BaseOrbital


class Fire(BaseOrbital):
    def __init__(self, player, radius=100, speed=0.1, duration=1000, cooldown=2000):
        super().__init__(player, speed=0, base_damage=30.0)

        self.radius = radius          
        self.angle = 0               
        self.angular_speed = speed   

        self.total_duration = duration 
        self.total_cooldown = cooldown
        self.timer_start = pygame.time.get_ticks()
        
        self.is_active_phase = True        

    def load_frames(self):
        for i in range(0, 6):
            img = pygame.image.load(f"assets/projectiles/fire/basic/sprite_{str(i)}.png").convert_alpha()
            self.frames.append(pygame.transform.scale(img, (40, 40)))

    def update_animation(self):
        if self.frame_count >= 60:
            self.frame_count = 0

        frame_intervals = [0, 10, 20, 30, 40, 50]
        frame_ids = [0, 1, 2, 3, 4, 5]

        for i in range(len(frame_intervals) - 1):
            if frame_intervals[i] <= self.frame_count < frame_intervals[i + 1]:
                self.active_frame = frame_ids[i]
                break

        self.frame_count += 1
        self.image = self.frames[self.active_frame]

    
    def update(self, enemies, *args, **kwargs):
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.timer_start

        if self.is_active_phase:
            if elapsed <= self.total_duration:
                self.update_animation()
                self.angle += self.angular_speed

                center_x = self.player.rect.centerx + math.cos(self.angle) * self.radius
                center_y = self.player.rect.centery + math.sin(self.angle) * self.radius

                self.rect.center = (center_x, center_y)
                hits = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_mask)
                for enemy in hits:
                    enemy.take_damage(self.base_damage) 
            else:
                self.is_active_phase = False
                self.timer_start = current_time
                self.rect.topleft = (-5000, -5000)

        else:
            if elapsed >= self.total_cooldown:
                self.is_active_phase = True
                self.timer_start = current_time

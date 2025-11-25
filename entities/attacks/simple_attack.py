import pygame
from entities.attacks.base_attack import BaseAttack


class SimpleAttack(BaseAttack):
    def __init__(self, player, speed=5):
        super().__init__(player, speed)

        self.total_time = 180  
        self.start_time = pygame.time.get_ticks()

        self.active_start = 40  
        self.active_end   = 120
        

    def load_frames(self):
        for i in range(0, 4):
            img = pygame.image.load(f"assets/attacks/player/sprite_{i}.png").convert_alpha()

            stretched = pygame.transform.scale(img, (200, 80))

            rotated = pygame.transform.rotate(stretched, -35)

            self.frames.append(rotated)

    def update_animation(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        percent = elapsed / self.total_time

        if percent < 0.25:
            self.active_frame = 0
        elif percent < 0.50:
            self.active_frame = 1
        elif percent < 0.75:
            self.active_frame = 2
        else:
            self.active_frame = 3

        self.image = self.frames[self.active_frame]

        if not self.player.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

        self.mask = pygame.mask.from_surface(self.image)

    def update(self, enemies: pygame.sprite.Group, *args, **kwargs):
        self.update_animation()
        offset_x = 70 if self.player.facing_right else -70
        offset_y = -5
        self.rect.centerx = self.player.rect.centerx + offset_x
        self.rect.centery = self.player.rect.centery + offset_y

        now = pygame.time.get_ticks()
        elapsed = now - self.start_time

        if self.active_start <= elapsed <= self.active_end:
            if not self.damage_done:
                hits = pygame.sprite.spritecollide(self, enemies, False, pygame.sprite.collide_mask)
                for enemy in hits:
                    self.on_hit(enemy)
                self.damage_done = True

        if elapsed >= self.total_time:
            self.kill()
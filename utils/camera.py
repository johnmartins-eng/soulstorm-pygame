import pygame


class Camera:
    def __init__(self, width, height):
        # width/height: viewport size (screen)
        # world_width/world_height: total world (background) size
        self.camera_rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.world_width = width
        self.world_height = height

    def apply(self, target: pygame.sprite.Sprite):
        return target.rect.move(-self.camera_rect.x, -self.camera_rect.y)

    def update_position(self, target: pygame.sprite.Sprite):
        x = target.rect.centerx - self.width // 2
        y = target.rect.centery - self.height // 2

        # Clamp to world bounds if available
        max_x = max(0, self.world_width - self.width)
        max_y = max(0, self.world_height - self.height)

        # ensure camera stays inside world
        x = max(0, min(x, max_x))
        y = max(0, min(y, max_y))

        self.camera_rect.x = int(x)
        self.camera_rect.y = int(y)

    def set_world_size(self, world_width: int, world_height: int):
        self.world_width = world_width
        self.world_height = world_height

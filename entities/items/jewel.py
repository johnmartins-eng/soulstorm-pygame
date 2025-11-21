import pygame


class Jewel(pygame.sprite.Sprite):
    def __init__(self, enemie_x, enemie_y):
        super().__init__()
        self.x = enemie_x
        self.y = enemie_y
        self.image: pygame.Surface = pygame.transform.scale(pygame.image.load(f"assets/items/Jewel.png").convert_alpha(), (25,25))
        self.rect: pygame.Rect = self.image.get_rect(topleft=(self.x, self.y))
        self.xp = 10

    def update(self, player, *args, **kwargs):
        if self.rect.colliderect(player):
            player.add_xp(self.xp)
            self.kill()
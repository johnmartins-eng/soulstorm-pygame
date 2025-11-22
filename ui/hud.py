import pygame

from screens.base_screen import BaseScreen

# Colors
BAR_BG_COLOR = (50, 50, 50)      # Dark Grey background for bars
XP_COLOR = (50, 150, 255)        # Bright Blue for XP
HP_COLOR = (200, 40, 40)         # Red for Health
BORDER_COLOR = (255, 255, 255)   # White border
TEXT_COLOR = (255, 255, 255)

class HUD(BaseScreen):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def draw(self, screen, player, camera):
        self.draw_xp_bar(screen, player)
        self.draw_health_bar(screen, player, camera)

    def draw_xp_bar(self, screen, player):
        bar_height = 20
        bar_width = self.screen_width
        
        if player.xp_to_next_level == 0:
            ratio = 0
        else:
            ratio = player.current_xp / player.xp_to_next_level
            ratio = min(1, max(0, ratio))

        bg_rect = pygame.Rect(0, 0, bar_width, bar_height)
        pygame.draw.rect(screen, BAR_BG_COLOR, bg_rect)

        fill_width = int(bar_width * ratio)
        fill_rect = pygame.Rect(0, 0, fill_width, bar_height)
        pygame.draw.rect(screen, XP_COLOR, fill_rect)

        pygame.draw.rect(screen, BORDER_COLOR, bg_rect, 2)


        level_text = f"LVL {player.level}" 
        text_surf = self.font_text.render(level_text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(bar_width - 50, bar_height // 2)) # Make the level text not centered, more at the right
        screen.blit(text_surf, text_rect)

    def draw_health_bar(self, screen, player, camera):
        screen_x = player.rect.centerx - camera.camera_rect.x
        screen_y = player.rect.bottom - camera.camera_rect.y + 2 

        width_bar = 50
        height_bar = 6
        
        ratio = player.health / player.max_health
        ratio = min(1, max(0, ratio))

        bg_rect = pygame.Rect(screen_x - width_bar // 2, screen_y, width_bar, height_bar)
        fill_rect = pygame.Rect(screen_x - width_bar // 2, screen_y, width_bar * ratio, height_bar)

        pygame.draw.rect(screen, BAR_BG_COLOR, bg_rect)
        pygame.draw.rect(screen, HP_COLOR, fill_rect)
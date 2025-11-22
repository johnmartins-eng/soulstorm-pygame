import pygame
import random
from screens.base_screen import BaseScreen
from ui.upgrade_data import UPGRADE_POOL

# --- RETRO COLOR PALETTE ---
COLOR_BG_OVERLAY = (0, 0, 0, 180)
COLOR_FRAME_OUTER = (50, 50, 150)
COLOR_FRAME_MID = (200, 200, 200)
COLOR_FRAME_INNER = (20, 20, 60)
COLOR_TEXT_TITLE = (255, 215, 0)
COLOR_TEXT_BODY = (255, 255, 255)
COLOR_HIGHLIGHT = (255, 100, 100)
COLOR_HOVER = (255, 255, 200)     

class LevelUpScreen(BaseScreen):
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_active = False
        self.current_choices = []
        
        self.card_rects = [] 

    def generate_choices(self):
        count = min(len(UPGRADE_POOL), 3)
        self.current_choices = random.sample(UPGRADE_POOL, count)
        self.is_active = True
        
        self.card_rects = []
        
        card_w, card_h = 200, 280
        spacing = 25
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        container_h = 450
        container_top = center_y - (container_h // 2)
        title_offset = 80 
        
        total_width = (card_w * count) + (spacing * (count - 1))
        start_x = center_x - (total_width // 2)
        card_y_pos = container_top + title_offset

        for i in range(len(self.current_choices)):
            card_x = start_x + i * (card_w + spacing)
            rect = pygame.Rect(card_x, card_y_pos, card_w, card_h)
            self.card_rects.append(rect)

    def select_option(self, index, player):
        if 0 <= index < len(self.current_choices):
            chosen_upgrade = self.current_choices[index]
            chosen_upgrade.effect_func(player)
            self.is_active = False
            self.current_choices = []
            self.card_rects = []

    def handle_input(self, event, player):
        if not self.is_active:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(self.card_rects):
                    if rect.collidepoint(mouse_pos):
                        self.select_option(i, player)

    def draw_retro_border_rect(self, surface, rect, thickness=4, is_hovered=False):
        outer_color = COLOR_HOVER if is_hovered else COLOR_FRAME_OUTER

        pygame.draw.rect(surface, outer_color, rect, width=thickness)
        
        inner_rect = rect.inflate(-thickness*2, -thickness*2)

        pygame.draw.rect(surface, COLOR_FRAME_MID, inner_rect, width=thickness//2)

        bg_rect = inner_rect.inflate(-thickness, -thickness)

        pygame.draw.rect(surface, COLOR_FRAME_INNER, bg_rect)

    def draw_text_wrapped(self, surface, text, color, rect, font):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] < rect.width - 10:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        y_offset = rect.top + 10
        for line in lines:
            img = font.render(line, False, color)
            surface.blit(img, (rect.left + 10, y_offset))
            y_offset += font.get_height() + 5

    def draw(self, screen):
        if not self.is_active:
            return

        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill(COLOR_BG_OVERLAY)
        screen.blit(overlay, (0, 0))

        container_w, container_h = 700, 450
        center_x, center_y = self.screen_width // 2, self.screen_height // 2
        container_rect = pygame.Rect(0, 0, container_w, container_h)
        container_rect.center = (center_x, center_y)
        
        pygame.draw.rect(screen, COLOR_FRAME_OUTER, container_rect, width=8)
        pygame.draw.rect(screen, "darkgray", container_rect.inflate(-16, -16))

        title_surf = self.title_font.render("LEVEL UP!", False, COLOR_TEXT_TITLE)
        title_rect = title_surf.get_rect(centerx=center_x, top=container_rect.top + 30)
        screen.blit(title_surf, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        for i, upgrade_data in enumerate(self.current_choices):
            if i >= len(self.card_rects): break
            
            card_rect = self.card_rects[i]
            
            is_hovered = card_rect.collidepoint(mouse_pos)

            self.draw_retro_border_rect(screen, card_rect, thickness=4, is_hovered=is_hovered)

            icon_size = 64
            icon_rect = pygame.Rect(0,0, icon_size, icon_size)
            icon_rect.centerx = card_rect.centerx
            icon_rect.top = card_rect.top + 50
            pygame.draw.rect(screen, COLOR_FRAME_MID, icon_rect, width=3)
            pygame.draw.rect(screen, upgrade_data.icon_color, icon_rect.inflate(-6,-6))

            name_color = COLOR_HOVER if is_hovered else COLOR_TEXT_TITLE
            name_surf = self.font_text.render(upgrade_data.name, False, name_color)
            screen.blit(name_surf, (card_rect.centerx - name_surf.get_width()//2, icon_rect.bottom + 15))
            
            desc_rect = pygame.Rect(card_rect.left, icon_rect.bottom + 40, card_rect.width, card_rect.height - 100)
            self.draw_text_wrapped(screen, upgrade_data.description, COLOR_TEXT_BODY, desc_rect, self.font_text)
import pygame

from screens.base_screen import BaseScreen


class GameOverScreen(BaseScreen):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.title_color = (220, 50, 50)
        self.outline_color = (0, 0, 0)
        self.overlay_target_alpha = 180

    def _render_text_outline(self, text, font, fg_color, outline_color, outline_width=2):
        main = font.render(text, True, fg_color)
        outline = font.render(text, True, outline_color)
        w = main.get_width() + outline_width * 2
        h = main.get_height() + outline_width * 2
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx == 0 and dy == 0:
                    continue
                surf.blit(outline, (dx + outline_width, dy + outline_width))
        surf.blit(main, (outline_width, outline_width))
        return surf

    def run(self):
        clock = pygame.time.Clock()
        w, h = self.screen.get_size()

        options = ["Reiniciar", "Sair"]
        selected = 0
        fade = 0

        while True:
            mouse_click_pos = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    # Removed ENTER and ESC shortcuts as requested: selection only by mouse
                    if event.key in (pygame.K_LEFT, pygame.K_UP):
                        selected = (selected - 1) % len(options)
                    if event.key in (pygame.K_RIGHT, pygame.K_DOWN):
                        selected = (selected + 1) % len(options)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click_pos = event.pos

            # Dark background + overlay (fade-in)
            self.screen.fill((16, 16, 16))
            if fade < self.overlay_target_alpha:
                fade = min(self.overlay_target_alpha, fade + 8)
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, fade))
            self.screen.blit(overlay, (0, 0))

            # Center panel
            panel_w = min(700, w - 120)
            panel_h = 320
            panel_rect = pygame.Rect((w - panel_w) // 2, (h - panel_h) // 2, panel_w, panel_h)
            panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel_surf.fill((30, 30, 30, 220))
            pygame.draw.rect(panel_surf, (40, 40, 40, 220), panel_surf.get_rect(), border_radius=12)
            self.screen.blit(panel_surf, panel_rect.topleft)

            # Title with outline
            title_surf = self._render_text_outline("GAME OVER", self.font_big, self.title_color, self.outline_color, outline_width=3)
            title_pos = title_surf.get_rect(center=(w // 2, panel_rect.top + 70))
            self.screen.blit(title_surf, title_pos)

            # Buttons
            btn_w, btn_h = 220, 64
            spacing = 40
            total_w = btn_w * len(options) + spacing * (len(options) - 1)
            start_x = w // 2 - total_w // 2
            btn_rects = []
            mx, my = pygame.mouse.get_pos()

            for i, opt in enumerate(options):
                rect = pygame.Rect(start_x + i * (btn_w + spacing), panel_rect.top + 170, btn_w, btn_h)
                btn_rects.append(rect)
                hover = rect.collidepoint((mx, my))
                is_selected = (selected == i)
                if hover or is_selected:
                    color = (200, 200, 200)
                    text_color = (24, 24, 24)
                else:
                    color = (120, 120, 120)
                    text_color = (240, 240, 240)

                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                txt = self.font_small.render(opt, True, text_color)
                self.screen.blit(txt, txt.get_rect(center=rect.center))

            # Handle mouse click on buttons
            if mouse_click_pos:
                for i, rect in enumerate(btn_rects):
                    if rect.collidepoint(mouse_click_pos):
                        return "retry" if i == 0 else "quit"

            pygame.display.flip()
            clock.tick(60)
            clock.tick(60)

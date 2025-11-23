import pygame
import sys

from screens.base_screen import BaseScreen

class RankingScreen(BaseScreen):
    def __init__(self, screen, width=800, height=600):
        super().__init__()
        self.screen = screen
        self.width = width
        self.height = height
        self.scroll_y = 0
        self.scroll_step = 30
    def run(self):
        clock = pygame.time.Clock()
        while True:
            mouse_click_pos = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    if event.key == pygame.K_UP:
                        self.scroll_y = max(0, self.scroll_y - self.scroll_step)
                    if event.key == pygame.K_DOWN:
                        self.scroll_y += self.scroll_step
                    if event.key == pygame.K_PAGEUP:
                        self.scroll_y = max(0, self.scroll_y - self.scroll_step * 5)
                    if event.key == pygame.K_PAGEDOWN:
                        self.scroll_y += self.scroll_step * 5

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click_pos = event.pos

                if event.type == pygame.MOUSEWHEEL:
                    # event.y: 1 (up) or -1 (down)
                    self.scroll_y = max(0, self.scroll_y - event.y * self.scroll_step)

            # desenha a tela
            self.draw()

            # processa clique após desenhar (button_rect é definido em draw)
            if mouse_click_pos and getattr(self, 'button_rect', None):
                if self.button_rect.collidepoint(mouse_click_pos):
                    return "menu"

            pygame.display.flip()
            clock.tick(60)

    def draw(self):
        self.screen.fill((30, 30, 30))

        # Título
        title_surface = self.title_font.render("RANKING", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 50))

        # Quadro para ranking
        panel_rect = pygame.Rect(self.width // 2 - 250, 150, 500, 300)
        pygame.draw.rect(self.screen, (50, 50, 50), panel_rect, border_radius=15)
        pygame.draw.rect(self.screen, (255, 255, 255), panel_rect, 3, border_radius=15)
        # Texto placeholder (apenas se não houver rows)
        try:
            from data import db
            rows = db.get_top_scores(100)
        except Exception:
            rows = []

        if not rows:
            placeholder = self.font_text.render("Nenhum dado disponível.", True, (200, 200, 200))
            self.screen.blit(placeholder, (self.width // 2 - placeholder.get_width() // 2, 300))
        else:
            # area de conteúdo
            content_top = panel_rect.top + 50
            content_left = panel_rect.left + 20
            content_width = panel_rect.width - 40
            content_height = panel_rect.height - 120

            row_h = 30
            total_h = len(rows) * row_h
            max_scroll = max(0, total_h - content_height)
            # clamp scroll
            if self.scroll_y < 0:
                self.scroll_y = 0
            if self.scroll_y > max_scroll:
                self.scroll_y = max_scroll

            # header
            header = self.font_text.render("Top 10", True, (200, 200, 200))
            self.screen.blit(header, (panel_rect.left + 20, panel_rect.top + 10))

            # draw visible rows
            for i, (username, score, ts) in enumerate(rows[:100]):
                y = content_top + i * row_h - self.scroll_y
                if y + row_h < content_top or y > content_top + content_height:
                    continue
                text = self.font_text.render(f"{i+1}. {username} — {score}", True, (220, 220, 220))
                self.screen.blit(text, (content_left, y))

            # scrollbar
            if total_h > content_height:
                bar_h = max(20, int(content_height * (content_height / total_h)))
                bar_x = panel_rect.right - 12
                bar_y = content_top + int((self.scroll_y / max_scroll) * (content_height - bar_h)) if max_scroll > 0 else content_top
                pygame.draw.rect(self.screen, (80, 80, 80), (bar_x, content_top, 8, content_height), border_radius=4)
                pygame.draw.rect(self.screen, (200, 200, 200), (bar_x, bar_y, 8, bar_h), border_radius=4)

        # Botão voltar
        self.button_rect = pygame.Rect(self.width // 2 - 100, 480, 200, 55)
        pygame.draw.rect(self.screen, (90, 90, 90), self.button_rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), self.button_rect, 2, border_radius=10)

        button_text = self.button_font.render("Voltar", True, (255, 255, 255))
        self.screen.blit(button_text, (
            self.button_rect.centerx - button_text.get_width() // 2,
            self.button_rect.centery - button_text.get_height() // 2
        ))

        # end draw
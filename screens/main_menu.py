import pygame

from screens.base_screen import BaseScreen

class MainMenu(BaseScreen):
    def __init__(self, screen, username):
        super().__init__()
        self.screen = screen
        self.username = username

        self.overlay_target_alpha = 180

    def run(self):
        clock = pygame.time.Clock()
        w, h = self.screen.get_size()

        fade = 0

        buttons = ["Iniciar", "Ranking", "Sair"]
        btn_w, btn_h = 200, 40
        spacing = 20

        while True:
            mouse_click_pos = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click_pos = event.pos

            # Fundo com fade
            self.screen.fill((16, 16, 16))
            if fade < self.overlay_target_alpha:
                fade = min(self.overlay_target_alpha, fade + 8)
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, fade))
            self.screen.blit(overlay, (0, 0))

            # Painel central
            panel_w = min(700, w - 120)
            panel_h = 360
            panel_rect = pygame.Rect((w-panel_w)//2, (h-panel_h)//2, panel_w, panel_h)

            panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel.fill((30, 30, 30, 220))
            pygame.draw.rect(panel, (40, 40, 40, 220), panel.get_rect(), border_radius=12)
            self.screen.blit(panel, panel_rect.topleft)

            # Título
            title = self.title_font.render("MENU PRINCIPAL", True, (230, 230, 230))
            self.screen.blit(title, title.get_rect(center=(w//2, panel_rect.top + 70)))

            # Saudar jogador
            text = self.font_small.render(f"Bem-vindo, {self.username}!", True, (210, 210, 210))
            self.screen.blit(text, text.get_rect(center=(w//2, panel_rect.top + 130)))

            # Botões
            total_w = btn_w * len(buttons) + spacing * (len(buttons)-1)
            start_x = w//2 - total_w//2

            btn_rects = []
            mx, my = pygame.mouse.get_pos()

            for i, opt in enumerate(buttons):
                rect = pygame.Rect(start_x + i*(btn_w+spacing), panel_rect.top + 210, btn_w, btn_h)
                btn_rects.append(rect)

                hover = rect.collidepoint((mx, my))

                color = (200,200,200) if hover else (120,120,120)
                text_color = (20,20,20) if hover else (240,240,240)

                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                t = self.font_small.render(opt, True, text_color)
                self.screen.blit(t, t.get_rect(center=rect.center))

            # Clique
            if mouse_click_pos:
                for i, rect in enumerate(btn_rects):

                    # Iniciar jogo
                    if rect.collidepoint(mouse_click_pos) and i == 0:
                        return "start"

                    # Ranking
                    if rect.collidepoint(mouse_click_pos) and i == 1:
                        return "ranking"

                    # Sair
                    if rect.collidepoint(mouse_click_pos) and i == 2:
                        return "quit"

            pygame.display.flip()
            clock.tick(60)

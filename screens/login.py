import pygame

from screens.base_screen import BaseScreen

class LoginScreen(BaseScreen):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.overlay_target_alpha = 180

        self.input_active = False
        self.username = ""

    def run(self):
        clock = pygame.time.Clock()
        w, h = self.screen.get_size()

        fade = 0

        input_rect = pygame.Rect(w//2 - 150, h//2 - 30, 300, 50)

        buttons = ["Entrar", "Sair"]
        btn_w, btn_h = 180, 55
        spacing = 40

        while True:
            mouse_click_pos = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit", None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_click_pos = event.pos

                    # Ativar/desativar input
                    if input_rect.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False

                if event.type == pygame.KEYDOWN and self.input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(self.username.strip()) > 0:
                            return "login", self.username.strip()
                    else:
                        if len(self.username) < 16:
                            self.username += event.unicode

            # Fundo escurecido com fade
            self.screen.fill((16, 16, 16))
            if fade < self.overlay_target_alpha:
                fade = min(self.overlay_target_alpha, fade + 8)
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, fade))
            self.screen.blit(overlay, (0, 0))

            # Painel central
            panel_w = min(700, w - 120)
            panel_h = 330
            panel_rect = pygame.Rect((w - panel_w)//2, (h - panel_h)//2, panel_w, panel_h)
            panel_surf = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
            panel_surf.fill((30, 30, 30, 220))
            pygame.draw.rect(panel_surf, (40, 40, 40, 220), panel_surf.get_rect(), border_radius=12)
            self.screen.blit(panel_surf, panel_rect.topleft)

            # Título
            title = self.title_font.render("LOGIN", True, (230, 230, 230))
            self.screen.blit(title, title.get_rect(center=(w//2, panel_rect.top + 70)))

            # Caixa de texto
            pygame.draw.rect(self.screen, (220, 220, 220), input_rect, border_radius=6)
            text_surf = self.font_text.render(self.username or "Digite seu nome...", True, (20, 20, 20))
            self.screen.blit(text_surf, (input_rect.x + 10, input_rect.y + 10))

            # Botões
            total_w = btn_w * len(buttons) + spacing * (len(buttons) - 1)
            start_x = w//2 - total_w//2
            btn_rects = []
            mx, my = pygame.mouse.get_pos()

            for i, opt in enumerate(buttons):
                rect = pygame.Rect(start_x + i*(btn_w+spacing), panel_rect.top + 220, btn_w, btn_h)
                btn_rects.append(rect)
                hover = rect.collidepoint((mx, my))

                color = (200,200,200) if hover else (120,120,120)
                text_color = (20,20,20) if hover else (240,240,240)

                pygame.draw.rect(self.screen, color, rect, border_radius=10)
                t = self.font_text.render(opt, True, text_color)
                self.screen.blit(t, t.get_rect(center=rect.center))

            # Clique
            if mouse_click_pos:
                for i, rect in enumerate(btn_rects):

                    # Entrar
                    if rect.collidepoint(mouse_click_pos) and i == 0:
                        if len(self.username.strip()) > 0:
                            return "login", self.username.strip()

                    # Sair
                    if rect.collidepoint(mouse_click_pos) and i == 1:
                        return "quit", None

            pygame.display.flip()
            clock.tick(60)

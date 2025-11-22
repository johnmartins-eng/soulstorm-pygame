import pygame

from screens.base_screen import BaseScreen

class PauseScreen(BaseScreen):
    def __init__(self, screen, width, height):
        super().__init__()
        self.screen = screen
        self.width = width
        self.height = height

        # Caixa central (mesmo estilo das suas telas)
        self.panel_rect = pygame.Rect(0, 0, 400, 350)
        self.panel_rect.center = (width // 2, height // 2)

        # Botões
        self.resume_button = pygame.Rect(0, 0, 260, 60)
        self.resume_button.center = (width // 2, height // 2 - 40)

        self.menu_button = pygame.Rect(0, 0, 260, 60)
        self.menu_button.center = (width // 2, height // 2 + 40)

    def draw_button(self, rect, text):
        pygame.draw.rect(self.screen, (60, 60, 60), rect, border_radius=10)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 3, border_radius=10)

        text_surface = self.button_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "resume"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.resume_button.collidepoint(event.pos):
                        return "resume"

                    if self.menu_button.collidepoint(event.pos):
                        return "menu"

            # camada escura como nas outras telas
            self.screen.fill((0, 0, 0))
            fade = pygame.Surface((self.width, self.height))
            fade.set_alpha(140)
            fade.fill((0, 0, 0))
            self.screen.blit(fade, (0, 0))

            # painel central
            pygame.draw.rect(self.screen, (40, 40, 40), self.panel_rect, border_radius=20)
            pygame.draw.rect(self.screen, (255, 255, 255), self.panel_rect, 4, border_radius=20)

            # título
            title_surface = self.title_font.render("PAUSADO", True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(self.width // 2, self.panel_rect.top + 70))
            self.screen.blit(title_surface, title_rect)

            # botões
            self.draw_button(self.resume_button, "Retomar")
            self.draw_button(self.menu_button, "Menu")

            pygame.display.flip()
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pause_screen = PauseScreen(screen, 800, 600)
    action = pause_screen.run()
    print(f"Pause screen action: {action}")
    pygame.quit()
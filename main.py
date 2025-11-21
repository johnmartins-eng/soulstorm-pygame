import math
from py_compile import main
import random
import sys
import pygame
from pygame.locals import *

from entities.attacks.simple_attack import SimpleAttack
from entities.enemies.skeleton import Skeleton
from entities.projectiles.fire import Fire
from screens.main_menu import MainMenu
from utils.camera import Camera
from entities.player import Player
from screens.game_over import GameOverScreen
from screens.login import LoginScreen
from screens.pause import PauseScreen
from screens.ranking import RankingScreen

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAY = (100, 100, 100)
FPS = 60

SPAWN_INTERVAL = 1500  # milliseconds (1.5 seconds)
PROJECTILE_SPAWN_INTERVAL = 2000  # ms

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Mostrar tela de login
    login = LoginScreen(screen)
    status, username = login.run()

    if status == "quit":
        pygame.quit()
        sys.exit()

    print("Jogador logado:", username)
        
    # Mostrar menu principal
    menu = MainMenu(screen, username)
    menu_choice = menu.run()

    if menu_choice == "quit":
        pygame.quit()
        sys.exit()

    if menu_choice == "ranking":
        print("Abrir tela de ranking (a fazer)")

    if menu_choice == "start":
        print("Iniciar o jogo agora")
    if menu_choice == "ranking":
        # Mostrar tela de ranking
        ranking_screen = RankingScreen(screen)
        ranking_choice = ranking_screen.run()

        if ranking_choice == "quit":
            pygame.quit()
            sys.exit()

        if ranking_choice == "menu":
            # Voltar ao menu principal
            menu = MainMenu(screen, username)
            menu_choice = menu.run()

            if menu_choice == "quit":
                pygame.quit()
                sys.exit()

            if menu_choice == "start":
                print("Iniciar o jogo agora")
    
    pygame.display.set_caption("NoName")
    clock = pygame.time.Clock()

    background = pygame.image.load("assets/backgrounds/bg.png").convert()
    background = pygame.transform.scale(background, (1600, 1600))

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    attacks = pygame.sprite.Group()
    items = pygame.sprite.Group()


    player = Player()
    all_sprites.add(player)

    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    last_spawn_time = pygame.time.get_ticks()
    last_projectile_spawn = pygame.time.get_ticks()

    app_running = True
    while app_running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

            # Aperta ESC → abre a tela de pause
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = PauseScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                result = pause.run()

                if result == "quit":
                    pygame.quit()
                    sys.exit()

                elif result == "menu":
                    # Voltar ao menu principal (sem passar pelo login)
                    menu = MainMenu(screen, username)
                    menu_choice = menu.run()

                    if menu_choice == "quit":
                        pygame.quit()
                        sys.exit()

                    if menu_choice == "start":
                        # reiniciar estado do jogo sem voltar ao login
                        player = Player()
                        all_sprites = pygame.sprite.Group()
                        enemies = pygame.sprite.Group()
                        projectiles = pygame.sprite.Group()
                        attacks = pygame.sprite.Group()
                        items = pygame.sprite.Group()
                        all_sprites.add(player)
                        camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
                        last_spawn_time = pygame.time.get_ticks()
                        last_projectile_spawn = pygame.time.get_ticks()
                        # interrompe o loop de eventos atual e continua o jogo com novo estado
                        break
                    # Se escolher Ranking a partir do menu, abrir a tela de Ranking
                    if menu_choice == "ranking":
                        ranking_screen = RankingScreen(screen)
                        ranking_choice = ranking_screen.run()

                        if ranking_choice == "quit":
                            pygame.quit()
                            sys.exit()

                        if ranking_choice == "menu":
                            # reabrir o menu principal
                            menu = MainMenu(screen, username)
                            menu_choice = menu.run()

                            if menu_choice == "quit":
                                pygame.quit()
                                sys.exit()

                            if menu_choice == "start":
                                player = Player()
                                all_sprites = pygame.sprite.Group()
                                enemies = pygame.sprite.Group()
                                projectiles = pygame.sprite.Group()
                                attacks = pygame.sprite.Group()
                                items = pygame.sprite.Group()
                                all_sprites.add(player)
                                camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
                                last_spawn_time = pygame.time.get_ticks()
                                last_projectile_spawn = pygame.time.get_ticks()
                                break

  
        if len(enemies) <= 20:
            if current_time - last_spawn_time >= SPAWN_INTERVAL:
                last_spawn_time = current_time
                radius = player.base_radius
                offset_x = random.uniform(-radius, radius)
                offset_y = random.uniform(-radius, radius)
                new_x = player.rect.x + offset_x
                new_y = player.rect.y + offset_y
                new_skeleton = Skeleton(x=new_x, y=new_y)
                all_sprites.add(new_skeleton)
                enemies.add(new_skeleton)


        player.update(attacks, all_sprites)

        if not player.alive():   # ele foi "kill()" no fim da animação
            from screens.game_over import GameOverScreen
            game_over = GameOverScreen(screen)
            choice = game_over.run()

            if choice == "retry":
                # reinicia o programa do zero (manter comportamento atual)
                pygame.quit()
                import os
                os.execl(sys.executable, sys.executable, *sys.argv)

            else:
                # ao invés de sair totalmente, voltar para o menu principal
                menu = MainMenu(screen, username)
                menu_choice = menu.run()

                if menu_choice == "quit":
                    pygame.quit()
                    sys.exit()
                if menu_choice == "start":
                    # reiniciar estado do jogo sem voltar ao login
                    player = Player()
                    all_sprites = pygame.sprite.Group()
                    enemies = pygame.sprite.Group()
                    projectiles = pygame.sprite.Group()
                    attacks = pygame.sprite.Group()
                    items = pygame.sprite.Group()
                    all_sprites.add(player)
                    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
                    last_spawn_time = pygame.time.get_ticks()
                    last_projectile_spawn = pygame.time.get_ticks()
                    # continue o loop principal com o novo estado
                    continue

                if menu_choice == "ranking":
                    ranking_screen = RankingScreen(screen)
                    ranking_choice = ranking_screen.run()

                    if ranking_choice == "quit":
                        pygame.quit()
                        sys.exit()

                    if ranking_choice == "menu":
                        # Voltar ao menu principal
                        menu = MainMenu(screen, username)
                        menu_choice = menu.run()

                        if menu_choice == "quit":
                            pygame.quit()
                            sys.exit()

                        if menu_choice == "start":
                            player = Player()
                            all_sprites = pygame.sprite.Group()
                            enemies = pygame.sprite.Group()
                            projectiles = pygame.sprite.Group()
                            attacks = pygame.sprite.Group()
                            items = pygame.sprite.Group()
                            all_sprites.add(player)
                            camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
                            last_spawn_time = pygame.time.get_ticks()
                            last_projectile_spawn = pygame.time.get_ticks()
                            continue

                # Para quaisquer outras opções, sair por segurança
                pygame.quit()
                sys.exit()

        attacks.update(enemies)

        enemies.update(player, items, all_sprites)

        items.update(player)

        camera.update_position(player)

        screen.fill(GRAY)
        screen.blit(background, (-camera.camera_rect.x, -camera.camera_rect.y))

        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        pygame.display.flip()

    pygame.quit()

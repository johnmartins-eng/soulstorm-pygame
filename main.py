import math
import random
import sys
import pygame
from pygame.locals import *

# --- IMPORTS ---
from entities.attacks.simple_attack import SimpleAttack
from entities.enemies.skeleton import Skeleton
from screens.main_menu import MainMenu
from utils.assets_load_manager import AssetsManager
from entities.player import Player
from screens.game_over import GameOverScreen
from screens.login import LoginScreen
from screens.pause import PauseScreen
from screens.ranking import RankingScreen
from data import db

# NEW IMPORT
from ui.levelup_screen import LevelUpScreen
from utils.game_context import GameContext

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAY = (100, 100, 100)
FPS = 60

SPAWN_INTERVAL = 1500
PROJECTILE_SPAWN_INTERVAL = 2000

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    login = LoginScreen(screen)
    status, username = login.run()

    if status == "quit":
        pygame.quit()
        sys.exit()

    print("Jogador logado:", username)

    # Initialize database and get/create current user
    db.init_db()
    current_user_id = db.get_or_create_user(username) if username else None

    # Mostrar menu principal em loop até o jogador escolher iniciar ou sair
    menu = MainMenu(screen, username)
    while True:
        menu_choice = menu.run()
        if menu_choice == "quit":
            pygame.quit()
            sys.exit()

        if menu_choice == "ranking":
            ranking_screen = RankingScreen(screen)
            ranking_choice = ranking_screen.run()
            if ranking_choice == "quit":
                pygame.quit()
                sys.exit()
            # ao retornar do ranking, reexibe o menu
            continue

        if menu_choice == "start":
            break

    assets: AssetsManager = AssetsManager.get_instance()
    game_context: GameContext = GameContext()

    pygame.display.set_caption("NoName")
    clock = pygame.time.Clock()

    background = pygame.image.load("assets/backgrounds/bg.png").convert()
    background = pygame.transform.scale(background, (1600, 1600))

    player = Player()
    game_context.add_player(player)

    level_up_screen: LevelUpScreen = LevelUpScreen(SCREEN_WIDTH, SCREEN_HEIGHT)

    last_spawn_time = pygame.time.get_ticks()
    last_projectile_spawn = pygame.time.get_ticks()

    app_running = True

    # --- MAIN GAME LOOP ---
    while app_running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

            if level_up_screen.is_active:
                level_up_screen.handle_input(event, game_context)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = PauseScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                result = pause.run()

                if result == "quit":
                    pygame.quit()
                    sys.exit()

                if result == "resume":
                    # volta ao jogo
                    pass

                if result == "menu":
                    # abrir menu principal (loop) e tratar opções
                    menu = MainMenu(screen, username)
                    while True:
                        menu_choice = menu.run()
                        if menu_choice == "quit":
                            pygame.quit()
                            sys.exit()
                        if menu_choice == "ranking":
                            ranking_screen = RankingScreen(screen)
                            ranking_choice = ranking_screen.run()
                            if ranking_choice == "quit":
                                pygame.quit()
                                sys.exit()
                            continue
                        if menu_choice == "start":
                            # RESET GAME
                            game_context.reset()
                            player = Player()
                            game_context.add_player(player)
                            level_up_screen = LevelUpScreen(
                                SCREEN_WIDTH, SCREEN_HEIGHT)
                            break
                    # continue the main loop with the new/reset state
                    continue

        # 2. UPDATE PHASE
        # Only update game logic if we are NOT choosing an upgrade
        if not level_up_screen.is_active:

            # A. Spawning Logic
            if len(game_context.enemies) <= (20 * player.level):
                if current_time - last_spawn_time >= SPAWN_INTERVAL/(1 + player.level/10):
                    last_spawn_time = current_time
                    radius = player.base_radius
                    offset_x = random.uniform(-radius, radius)
                    offset_y = random.uniform(-radius, radius)
                    new_x = player.rect.x + offset_x
                    new_y = player.rect.y + offset_y
                    new_skeleton = Skeleton(
                        x=new_x, y=new_y, player_level=player.level, assets=assets.get_images("skeleton"))
                    game_context.all_sprites.add(new_skeleton)
                    game_context.enemies.add(new_skeleton)

            # B. Entity Updates
            game_context.player.update(game_context)
            game_context.attacks.update(game_context.enemies)
            game_context.enemies.update(game_context)
            game_context.items.update(player)
            game_context.orbitals.update(game_context.enemies)

            if player.leveled_up:
                level_up_screen.generate_choices()
                player.leveled_up = False

            game_context.camera.update_position(player)

        # 3. DRAW PHASE
        screen.fill(GRAY)
        screen.blit(background, (-game_context.camera.camera_rect.x, -
                    game_context.camera.camera_rect.y))

        for sprite in game_context.all_sprites:
            screen.blit(sprite.image, game_context.camera.apply(sprite))

        # DRAW HUD
        if not level_up_screen.is_active:
            game_context.hud.draw(screen, player, game_context.camera)

        # DRAW LEVEL UP
        if level_up_screen.is_active:
            level_up_screen.draw(screen)

        if not player.alive():
            from screens.game_over import GameOverScreen
            game_over = GameOverScreen(screen)
            choice = game_over.run()

            # Save player's score (use current_xp as score)
            try:
                if current_user_id is not None:
                    db.add_score(current_user_id, game_context.player.total_xp)
            except Exception:
                pass
            if choice == "retry":
                # Reset everything and continue playing
                game_context.reset()
                player = Player()
                game_context.add_player(player)
                level_up_screen.is_active = False
                continue

            if choice == "menu":
                # Voltar ao menu principal (loop) e tratar opções
                menu = MainMenu(screen, username)
                while True:
                    menu_choice = menu.run()
                    if menu_choice == "quit":
                        pygame.quit()
                        sys.exit()
                    if menu_choice == "ranking":
                        ranking_screen = RankingScreen(screen)
                        ranking_choice = ranking_screen.run()
                        if ranking_choice == "quit":
                            pygame.quit()
                            sys.exit()
                        continue
                    if menu_choice == "start":
                        # Reset game and resume
                        game_context.reset()
                        player = Player()
                        game_context.add_player(player)
                        level_up_screen.is_active = False
                        break
                # after returning from menu, continue main loop with new state
                continue

            # any other response -> quit
            pygame.quit()
            sys.exit()

        pygame.display.flip()

    pygame.quit()

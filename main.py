import math
import random
import sys
import pygame
from pygame.locals import *

# --- IMPORTS ---
from entities.attacks.simple_attack import SimpleAttack
from entities.enemies.skeleton import Skeleton
from entities.projectiles.fire import Fire
from screens.main_menu import MainMenu
from ui.hud import HUD
from utils.camera import Camera
from entities.player import Player
from screens.game_over import GameOverScreen
from screens.login import LoginScreen
from screens.pause import PauseScreen
from screens.ranking import RankingScreen

# NEW IMPORT
from ui.levelup_screen import LevelUpScreen

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

    menu = MainMenu(screen, username)
    menu_choice = menu.run()

    if menu_choice == "quit":
        pygame.quit()
        sys.exit()

    if menu_choice == "ranking":
        ranking_screen = RankingScreen(screen)
        ranking_choice = ranking_screen.run()
        if ranking_choice == "quit":
            pygame.quit(); sys.exit()

    pygame.display.set_caption("NoName")
    clock = pygame.time.Clock()

    background = pygame.image.load("assets/backgrounds/bg.png").convert()
    background = pygame.transform.scale(background, (1600, 1600))

    # Initialize Groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    attacks = pygame.sprite.Group()
    items = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    hud = HUD(SCREEN_WIDTH, SCREEN_HEIGHT)
    
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
                level_up_screen.handle_input(event, player)
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause = PauseScreen(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
                result = pause.run()

                if result == "quit":
                    pygame.quit(); sys.exit()
                
                elif result == "menu":
                    menu = MainMenu(screen, username)
                    menu_choice = menu.run()
                    if menu_choice == "start":
                        # RESET GAME
                        player = Player()
                        all_sprites = pygame.sprite.Group()
                        enemies = pygame.sprite.Group()
                        items = pygame.sprite.Group()
                        attacks = pygame.sprite.Group()
                        all_sprites.add(player)
                        level_up_screen = LevelUpScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
                        continue 

        # 2. UPDATE PHASE
        # Only update game logic if we are NOT choosing an upgrade
        if not level_up_screen.is_active:
            
            # A. Spawning Logic
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

            # B. Entity Updates
            player.update(attacks, all_sprites)
            attacks.update(enemies)
            enemies.update(player, items, all_sprites)
            items.update(player)

            if player.leveled_up:
                level_up_screen.generate_choices()
                player.leveled_up = False

            camera.update_position(player)

        # 3. DRAW PHASE
        screen.fill(GRAY)
        screen.blit(background, (-camera.camera_rect.x, -camera.camera_rect.y))

        for sprite in all_sprites:
            screen.blit(sprite.image, camera.apply(sprite))

        # DRAW HUD
        if not level_up_screen.is_active:
            hud.draw(screen, player, camera)

        # DRAW LEVEL UP
        if level_up_screen.is_active:
            level_up_screen.draw(screen)

        if not player.alive():
                from screens.game_over import GameOverScreen
                game_over = GameOverScreen(screen)
                choice = game_over.run()
                
                if choice == "retry":
                    # Reset everything
                    player = Player()
                    all_sprites = pygame.sprite.Group()
                    enemies = pygame.sprite.Group()
                    items = pygame.sprite.Group()
                    attacks = pygame.sprite.Group()
                    all_sprites.add(player)
                    camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
                    level_up_screen.is_active = False
                elif choice == "menu":
                    pass
                else:
                    pygame.quit(); sys.exit()

        pygame.display.flip()

    pygame.quit()
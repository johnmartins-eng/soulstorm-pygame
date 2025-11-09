import math
import pygame
from pygame.locals import *


SCREEN_WIDTH =  900
SCREEN_HEIGHT = 500 

# --- Cores ---
BLACK = (10, 10, 10)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN_LIGHT = (50, 200, 50)
GOLD = (255, 215, 0)
PRESSED_COLOR = (100, 100, 255)
HIT_COLOR = (255, 50, 50)

FPS = 60

PLAYER_X = 400
PLAYER_Y = 200

X_SPEED = 5
Y_SPEED = 5

frames = []
# idle-animation
for i in range(0,6):
    frames.append("assets/character/idle/sprite_0" + str(i) + ".png")

# running-animation
for i in range(6, 14):
    if i < 10:
        frames.append("assets/character/running/sprite_0" + str(i) + ".png")
    else:
        frames.append("assets/character/running/sprite_" + str(i) + ".png")

active_frame = 0
mode = 0 # 0 = idle, 1 = running right, 2 = running left, 3 = running up, 4 = running down 
count = 0

def update_player(mod, counter):
    if counter >= 60:
        counter = 0
    if mod == 0:
        if counter <= 10:
            act = 0
        elif counter <= 20:
            act = 1
        elif counter <= 30:
            act = 2
        elif counter <= 40:
            act = 3
        elif counter <= 50:
            act = 4
        elif counter <= 60:
            act = 5
    
    if mod == 1:
        if counter <= 7.5:
            act = 6
        elif counter <= 15:
            act = 7
        elif counter <= 22.5:
            act = 8
        elif counter <= 30:
            act = 9
        elif counter <= 37.5:
            act = 10
        elif counter <= 45:
            act = 11
        elif counter <= 52.5:
            act = 12
        elif counter <= 60:
            act = 12
        
    counter += 1
    return act, counter

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("NoName")
    clock = pygame.time.Clock()

    app_running = True
    facing_right = True 

    while app_running:
        clock.tick(FPS)
        screen.fill(GRAY)

        keys = pygame.key.get_pressed()

        dx = dy = 0
        if keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_s]:
            dy = 1
        if keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_d]:
            dx = 1

        moving = dx != 0 or dy != 0

        if moving:
            length = math.sqrt(dx * dx + dy * dy)
            dx /= length
            dy /= length
            PLAYER_X += dx * X_SPEED
            PLAYER_Y += dy * Y_SPEED

        if not moving:
            mode = 0  # idle
        else:
            mode = 1  # running

            if dx > 0:
                facing_right = True
            elif dx < 0:
                facing_right = False

        active_frame, count = update_player(mode, count)
        player = pygame.transform.scale(pygame.image.load(frames[active_frame]), (70, 70))

        if not facing_right:
            player = pygame.transform.flip(player, True, False)

        screen.blit(player, (PLAYER_X, PLAYER_Y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                app_running = False

        pygame.display.flip()

    pygame.quit()

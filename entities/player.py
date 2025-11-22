import pygame
import math

from entities.attacks.simple_attack import SimpleAttack
from entities.base_entity import AnimationModeEnum, BaseEntity
from utils.direction_enum import DirectionEnum

START_POS_X = 400
START_POS_Y = 200

PLAYER_SPEED = 5

BASE_RADIUS = 200  # Pixels


class Player(BaseEntity):
    def __init__(self):
        super().__init__(x=START_POS_X, y=START_POS_Y,
                         health=200, base_damage=400, speed=3.0)
        self.base_radius = BASE_RADIUS  # Pixels

        self.attack_cooldown = 1400 
        self.last_attack_time = 0

        self.max_health = 200

        self.level = 1
        self.current_xp = 0
        self.xp_to_next_level = 100
        self.leveled_up = False

    def load_frames(self):
        # idle frames
        for i in range(0, 6):
            img = pygame.image.load(
                f"assets/character/idle/sprite_0{i}.png").convert_alpha()
            self.frames.append(pygame.transform.scale(img, (70, 70)))

        # running frames
        for i in range(6, 14):
            name = f"sprite_0{i}.png" if i < 10 else f"sprite_{i}.png"
            img = pygame.image.load(
                f"assets/character/running/{name}").convert_alpha()
            self.frames.append(pygame.transform.scale(img, (70, 70)))

        # dying frames
        for i in range(37, 47):
            img = pygame.image.load(
                f"assets/character/dying/sprite_{i}.png").convert_alpha()
            self.frames.append(pygame.transform.scale(img, (70, 70)))

    def update_animation(self):
        if self.animation_mode != AnimationModeEnum.DYING and self.frame_count >= 60:
            self.frame_count = 0

        if self.animation_mode == AnimationModeEnum.IDLE:  # idle
            frame_intervals = [0, 10, 20, 30, 40, 50, 60]
            frame_ids = [0, 1, 2, 3, 4, 5]
        elif self.animation_mode == AnimationModeEnum.RUNNING:  # running
            frame_intervals = [0, 7.5, 15, 22.5, 30, 37.5, 45, 52.5]
            frame_ids = [6, 7, 8, 9, 10, 11, 12]
        elif self.animation_mode == AnimationModeEnum.DYING:
            frame_intervals = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60]
            frame_ids = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22]

        for i in range(len(frame_intervals) - 1):
            if frame_intervals[i] <= self.frame_count < frame_intervals[i + 1]:
                self.active_frame = frame_ids[i]
                break

        self.frame_count += 1

        self.image = self.frames[self.active_frame]
        if not self.facing_right:
            self.image = pygame.transform.flip(self.image, True, False)

    def __handle_input(self):
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
            self.animation_mode = AnimationModeEnum.RUNNING

            length = math.sqrt(dx * dx + dy * dy)
            dx /= length
            dy /= length
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

            if dx > 0:
                self.facing_right = True
            elif dx < 0:
                self.facing_right = False
        else:
            self.animation_mode = AnimationModeEnum.IDLE

        self.change_direction(dx, dy)

    def __try_auto_attack(self, attacks_group, all_sprites_group):
        now = pygame.time.get_ticks()
        if now - self.last_attack_time >= self.attack_cooldown:
            self.last_attack_time = now
            attack = SimpleAttack(self)
            attacks_group.add(attack)
            all_sprites_group.add(attack)

    def update(self, attacks_group=None, all_sprites_group=None, *args, **kwargs):
        if self.dying:
            self.update_animation()
            if self.frame_count >= 60:
                self.kill()
            return

        self.__handle_input()
        self.update_animation()

        if attacks_group is not None and all_sprites_group is not None:
            self.__try_auto_attack(attacks_group, all_sprites_group)

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0 and not self.dying:
            self.animation_mode = AnimationModeEnum.DYING
            self.frame_count = 0
            self.dying = True

    def change_direction(self, dx: int, dy: int):
        if dx == 1 and dy == 0:
            self.direction = DirectionEnum.RIGHT

        if dx == -1 and dy == 0:
            self.direction = DirectionEnum.LEFT

        if dx == 0 and dy == 1:
            self.direction = DirectionEnum.UP

        if dx == 0 and dy == -1:
            self.direction = DirectionEnum.DOWN

        if dx == 1 and dy == 1:
            self.direction = DirectionEnum.DIAGONAL_RIGHT_UP

        if dx == 1 and dy == -1:
            self.direction = DirectionEnum.DIAGONAL_RIGHT_DOWN

        if dx == -1 and dy == -1:
            self.direction = DirectionEnum.DIAGONAL_LEFT_DOWN

        if dx == -1 and dy == 1:
            self.direction = DirectionEnum.DIAGONAL_LEFT_UP

    # Experience and Leveling System
    def add_xp(self, amount):
        self.current_xp += amount
        if self.current_xp >= self.xp_to_next_level:
            self.level_up()
            return True  # Sinaliza que o jogador subiu de nível
        return False

    def level_up(self):
        self.level += 1 
        self.xp_to_next_level += 100
        print(f"Level {self.level} reached!")
        self.leveled_up = True

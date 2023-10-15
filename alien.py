import random
import os

import pygame
from pygame.sprite import Group

from laser import Laser

PATH = os.path.abspath('.') + '/graphics/'


class Alien(pygame.sprite.Sprite):
    direction: int
    health: int

    def __init__(self, pos: tuple[float, float], color='red'):
        super().__init__()
        file_path = PATH + color + '.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.direction = 1
        self.lasers = pygame.sprite.Group()
        self.health = 1

    def update(self, game: 'Game'):
        self.check_collision(game)
        self.lasers.update()
        self.lasers.draw(pygame.display.get_surface())
        self.rect.x += self.direction
        # using random number to shoot lasers
        if not pygame.time.get_ticks() % 100 and random.randint(0, 50) == 0:
            self.shoot_laser()
        if self.rect.right >= pygame.display.get_surface().get_width() or self.rect.left <= 0:
            self.rect.y += 10
            self.direction *= -1

    def shoot_laser(self):
        laser = Laser(self.rect.center, 8)
        self.lasers.add(laser)

    def hurt(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.kill()

    def check_collision(self, game: 'Game'):
        if game.blocks:
            self.check_collision_with_group(game.blocks, True)
        if game.player:
            if self.check_collision_with_group(game.player):
                if hasattr(game.player.sprite, 'hurt'):
                    game.player.sprite.hurt(1)

    def check_collision_with_group(self, group: Group, do_kill=False) -> bool:
        """ check collision with given group """
        if self.lasers:
            for laser in self.lasers:
                if pygame.sprite.spritecollide(laser, group, do_kill):
                    laser.kill()
                    return True
            return False
        if pygame.sprite.spritecollide(self, group, do_kill):
            return True
        return False

    @staticmethod
    def setup_aliens(rows=5, cols=8, x_offset=60, y_offset=48, x_start=100, y_start=100) -> pygame.sprite.Group:
        aliens = pygame.sprite.Group()
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_offset + x_start
                y = row_index * y_offset + y_start
                if row_index == 0:
                    aliens.add(Alien((x, y), 'yellow'))
                elif row_index == 1:
                    aliens.add(Alien((x, y), 'green'))
                else:
                    aliens.add(Alien((x, y), 'red'))
        return aliens


class Extra(pygame.sprite.Sprite):
    direction: int
    health: int

    def __init__(self, side: str):
        super().__init__()
        file_path = PATH + 'extra.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        # based on side, set x position -50 or +50
        x = 50 if side == 'left' else pygame.display.get_surface().get_width() - 50
        pos = (x, 15)
        self.rect = self.image.get_rect(topleft=pos)
        # based on side, set direction
        self.direction = 3 if side == 'left' else -3
        self.lasers = pygame.sprite.Group()
        self.health = 2

    def update(self, game: 'Game'):
        self.check_collision(game)
        self.lasers.update()
        self.lasers.draw(pygame.display.get_surface())
        self.rect.x += self.direction
        # using random number to shoot lasers
        if not pygame.time.get_ticks() % 100 and random.randint(0, 3) == 0:
            self.shoot_laser()
        if self.rect.right >= pygame.display.get_surface().get_width() or self.rect.left <= 0:
            self.direction *= -1

    def shoot_laser(self):
        laser = Laser(self.rect.center, 10)
        self.lasers.add(laser)

    def hurt(self, damage: int):
        self.health -= damage
        print(f"Extra enemy health: {self.health}")
        if self.health <= 0:
            self.kill()

    def check_collision(self, game: 'Game'):
        if game.blocks:
            self.check_collision_with_group(game.blocks, True)
        if game.player:
            if self.check_collision_with_group(game.player):
                # check if this object has method hurt
                if hasattr(game.player.sprite, 'hurt'):
                    game.player.sprite.hurt(1)

    def check_collision_with_group(self, group: Group, do_kill=False) -> bool:
        """ check collision with given group """
        if self.lasers:
            for laser in self.lasers:
                if pygame.sprite.spritecollide(laser, group, do_kill):
                    laser.kill()
                    return True
            return False
        return False

    @staticmethod
    def spawn_extra_alien(extra_list: Group):
        """ added Extra enemy every 800 ticks """
        spawn_time = 800
        if not pygame.time.get_ticks() % spawn_time and len(extra_list) < 3:
            extra_list.add(Extra(random.choice(('left', 'right'))))
            print(f"Extra enemy spawned: {len(extra_list)}")

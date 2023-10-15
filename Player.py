import sys

import pygame

from laser import Laser


# Player inherits from pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    health: int

    def __init__(self, pos: tuple[float, float]):
        super().__init__()
        print(f"Player created at {pos}")
        self.image = pygame.image.load("./graphics/player.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = 5
        self.ready = True
        self.laser_timer = 0
        self.laser_cooldown = 500
        self.lasers = pygame.sprite.Group()
        self.health = 3

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.centerx += self.speed
        elif keys[pygame.K_LEFT]:
            self.rect.centerx -= self.speed
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_timer = pygame.time.get_ticks()

    def cooldown(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_timer >= self.laser_cooldown:
                self.ready = True

    def update(self, game: 'Game'):
        self.input()
        self.rect.clamp_ip(pygame.display.get_surface().get_rect())
        self.cooldown()
        self.lasers.update()
        self.check_collision(game)

    def shoot_laser(self):
        laser = Laser(self.rect.center, -10)
        self.lasers.add(laser)

    def check_collision(self, game: 'Game'):
        if game.blocks:
            self.check_collision_with_group(game.blocks, True)
        if game.aliens:
            self.check_collision_with_group(game.aliens, True)
        if game.extra_aliens:
            self.check_collision_with_group(game.extra_aliens, True)

    def check_collision_with_group(self, group: pygame.sprite.Group, do_kill=False) -> bool:
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

    def hurt(self, damage: int):
        print(f"Player hurt by {damage}")
        self.health -= damage
        if self.health <= 0:
            print("Game Over!")
            self.kill()
            sys.exit()

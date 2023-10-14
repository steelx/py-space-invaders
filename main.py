import sys
import pygame

from alien import Alien, Extra
from Player import Player
from obstacles import Block


# space invaders game using pygame


class Game:
    def __init__(self, screen_: pygame.Surface):
        self.screen = screen_
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        player_sprite = Player((screen_width / 2, screen_height - 25))
        self.player = pygame.sprite.GroupSingle(player_sprite)
        obstacles_count = 4
        obstacles_x_position = [num * (screen_width / obstacles_count) for num in range(obstacles_count)]
        self.blocks: pygame.sprite.Group = Block.create_block_obstacles(
            *obstacles_x_position, x_start=screen_width / 15, y_start=screen_mode[1] - 175)
        self.aliens = Alien.setup_aliens(x_start=screen_width / 15, y_start=screen_height / 10)
        self.extra_aliens = pygame.sprite.Group()

    def run(self):
        self.player.update()
        self.blocks.update()
        self.aliens.update()
        Extra.spawn_extra_alien(self.extra_aliens)
        self.extra_aliens.update()

        self.player.draw(self.screen)
        self.player.sprite.lasers.draw(self.screen)
        self.blocks.draw(self.screen)
        self.aliens.draw(self.screen)
        self.extra_aliens.draw(self.screen)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Space Invaders")
    screen_mode = (1024, 720)
    screen = pygame.display.set_mode(screen_mode)
    clock = pygame.time.Clock()
    game = Game(screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((30, 30, 30))
        game.run()
        pygame.display.flip()
        clock.tick(60)

import pygame
from typing import Union


class Block(pygame.sprite.Sprite):
    """Block class for creating obstacles, inherits from pygame.sprite.Sprite"""
    SHAPE = [
        '  xxxxxxx  ',
        ' xxxxxxxxx ',
        'xxxxxxxxxxx',
        'xxxxxxxxxxx',
        'xxxxxxxxxxx',
        'xxx     xxx',
        'xx       xx',
    ]

    angle = 0

    def __init__(self, size: int, color: [int, int, int], pos: tuple[int, int]):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=pos)

    @staticmethod
    def create_block_obstacle(size: int, color: [int, int, int], x_start: float, y_start: float, x_offset=5):
        """
        This creates a single Block from given Shape
        such that it can be broken into pieces
        :return Block:
        """
        blocks = pygame.sprite.Group()
        for row_index, row in enumerate(Block.SHAPE):
            for col_index, col in enumerate(row):
                if col == 'x':
                    x = col_index * size + x_start + x_offset
                    y = row_index * size + y_start
                    blocks.add(Block(10, color, (x, y)))
        return blocks

    @staticmethod
    def create_block_obstacles(*offset: Union[int, ...], x_start: float, y_start: float) -> pygame.sprite.Group:
        blocks = pygame.sprite.Group()
        x_offset: int
        for x_offset in offset:
            blocks.add(Block.create_block_obstacle(8, (241, 79, 80), x_start, y_start, x_offset))
        return blocks

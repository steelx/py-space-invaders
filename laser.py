import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[float, float], speed: int):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= -50 or self.rect.y >= pygame.display.get_surface().get_height() + 50:
            self.kill()

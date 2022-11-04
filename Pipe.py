import pygame
from Enumeration import PipeColor

class Pipe(pygame.sprite.Sprite):
    def __init__(self,color:PipeColor):
        super().__init__()
        if color == PipeColor.GREEN:
            self.image = pygame.transform.scale2x(pygame.image.load('assets/images/pipe/pipe-green.png').convert_alpha())
        else:
            self.image = pygame.transform.scale2x(
                pygame.image.load('assets/images/pipe/pipe-red.png').convert_alpha())
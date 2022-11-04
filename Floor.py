import pygame


class Floor(pygame.sprite.Sprite):
    def __init__(self, screen:pygame.Surface):
        super().__init__()
        self.screen = screen
        self.image = pygame.image.load('assets/images/floor/base.png').convert_alpha()
        self.image = pygame.transform.scale2x(self.image)
        self.position_x = 0

    def draw(self):
        self.screen.blit(self.image, (self.position_x, self.screen.get_height() - 100))
        self.screen.blit(
            self.image, (self.position_x + self.screen.get_width(), self.screen.get_height() - 100))

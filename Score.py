import pygame


class Score():
    def __init__(self):
        super().__init__()
        self.number = [
            pygame.image.load('assets/images/numbers/0.png').convert_alpha(),
            pygame.image.load('assets/images/numbers/1.png').convert_alpha(),
            pygame.image.load('assets/images/numbers/2.png').convert_alpha(),
            pygame.image.load('assets/images/numbers/3.png').convert_alpha(),
            pygame.image.load('assets/images/numbers/4.png').convert_alpha(),
            pygame.image.load('assets/images/numbers/5.png').convert_alpha(),
            pygame.image.load('assets/images/numbers/6.png').convert_alpha(),
            pygame.image.load('assets/images/numbers/7.png').convert_alpha(),
            pygame.image.load('assets/images/numbers/8.png').convert_alpha(),
            pygame.image.load('assets/images/numbers/9.png').convert_alpha(),
        ]


    def get_score(self, score: int) -> list[pygame.Surface]:
        str_surface = list()
        for num in str(score):
            str_surface.append( self.number[int(num)])
        return str_surface

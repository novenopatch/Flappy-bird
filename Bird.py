import pygame


class Bird(pygame.sprite.Sprite):
    def __init__(self, screen: pygame.Surface,bird_frames:list[pygame.Surface]=None):
        super().__init__()

        self.screen = screen
        self.bird_frames = bird_frames
        self.bird_index = 0
        self.image = self.bird_frames[self.bird_index]
        self.rect = self.center_bird_rect()
        self.gravity = 0.25
        self.bird_movement = 0


    def draw(self):
        self.update()
        self.screen.blit(self.rotated_bird, self.rect)

    def update(self):
        self.bird_movement += self.gravity
        self.rotated_bird = self.rotate_bird()
        self.rect.centery += self.bird_movement
    def rotate_bird(self)->pygame.Surface:
        return  pygame.transform.rotozoom(self.image, -self.bird_movement * 3, 1)
        # return pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    def update_movement(self):
        self.bird_movement = 0
        self.bird_movement -= 7

    def center_bird_rect(self) -> pygame.Rect:
        return self.image.get_rect(center=(int(self.screen.get_width() / 5), int(self.screen.get_height() / 2)))



    def bird_animation(self):
        self.image = self.bird_frames[self.bird_index]
        self.rect = self.image.get_rect(center=((self.screen.get_width() - 76) / 5, self.rect.centery))

    def on_event_bird_flap(self):
        if self.bird_index < 2:
            self.bird_index += 1
        else:
            self.bird_index = 0
        self.bird_animation()

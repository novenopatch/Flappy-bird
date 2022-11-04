import pygame, random
from Bird import Bird
from Floor import Floor
from Pipe import Pipe
from Sounds import SoundManager
from Enumeration import *
from Save import Save
from Score import  Score
from Level import Level

class Game():
    def __init__(self, screen: pygame.Surface,levels:list[Level]):
        self.screen: pygame.Surface = screen
        self.screen_width: int = screen.get_width()
        self.screen_height: int = screen.get_height()
        self.game_font: pygame.font.Font = pygame.font.Font("assets/font/Pixeled.ttf", 20)
        self.game_state:GameState  = GameState.IS_PAUSE
        self.current_level_int:int = 1
        self.levels:list[Level] = levels
        self.current_level:Level = self.levels[self.current_level_int-1]
        self.bird_sprite: Bird = Bird(screen,self.current_level.bird_frames)
        self.bg: pygame.Surface = self.current_level.BG
        self.pipe_height: list[int] = self.current_level.PIPE_HEIGHT_LIST
        self.pipe_spacing: int = self.current_level.PIPE_SPACING

        self.bird: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle(self.bird_sprite)

        self.game_starting: pygame.Surface = pygame.transform.scale2x(
            pygame.image.load('assets/images/message.png').convert_alpha())

        self.game_over = pygame.transform.scale2x(
            pygame.image.load('assets/images/gameover.png').convert_alpha())
        self.game_over_rect: pygame.Rect = self.game_over.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2))
        self.game_starting_rect: pygame.Rect = self.game_starting.get_rect(
            center=(self.screen_width / 2, self.screen_height / 2))
        self.floor: Floor = Floor(screen)
        self.save:Save = Save()
        self.score: int = self.save.get_data(SaveData.SCORE)
        self.high_score: int = self.save.get_data(SaveData.HIGH_SCORE)
        self.pipe: Pipe = self.current_level.pipe
        self.pipes: list[pygame.Rect] = []

        self.pipe_starting_pos_x: int = 700
        self.score_sound_countdown: int = 200
        self.sounds_manager: SoundManager = SoundManager()

    def run(self):
        self.bird.sprite.draw()
        ##game
        self.game_state = self.check_collision()
        self.pipes = self.move_pipes()
        self.draw_pipes()
        self.score_display()
        self.score, self.high_score = self.update_score()
        self.score_sound_countdown -= 1
        if self.score_sound_countdown <= 0:
            self.score_sound_countdown = 200
            self.sounds_manager.play(Sounds.SCORE)
        self.floor.position_x -= 1
        self.floor.draw()

    def update_screen_on_start_new_level(self):
        self.update_elements()
        self.game_state = GameState.IS_PLAYING
    def update_elements(self):
        self.current_level = self.levels[self.current_level_int - 1]
        self.bird_sprite: Bird = Bird(self.screen, self.current_level.bird_frames)
        self.bird: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle(self.bird_sprite)
        self.bg: pygame.Surface = self.current_level.BG
        self.pipe: Pipe = self.current_level.pipe
        self.pipe_height: list[int] = self.current_level.PIPE_HEIGHT_LIST
        self.pipe_spacing: int = self.current_level.PIPE_SPACING
    def update_screen_on_over_game(self):
        self.current_level_int = 1
        self.update_elements()
        self.screen.blit(self.game_over, self.game_over_rect)
        self.score_display()
    def update_screen_on_pause_game(self):
        self.screen.blit(self.game_starting, self.game_starting_rect)
        self.score_display()
    def update_floor_position(self):
        if self.floor.position_x <= -self.screen_width:
            self.floor.position_x = 0

    def update_score(self) -> tuple:
        self.score += 0.01
        if self.score > self.high_score:
            self.high_score = self.score
        if self.score >= self.current_level.high_score and self.current_level_int<len(self.levels):
            self.current_level_int +=1
            self.game_state = GameState.IS_END_LEVEl_AND_GO_TO_NEXT_LEVEL
            print(self.current_level_int)

        return self.score, self.high_score

    def display_level(self):
        level_surface = self.game_font.render(self.current_level.name, True, (255, 255, 255))
        level_rect = level_surface.get_rect(center=(288, 50))
        self.screen.blit(level_surface, level_rect)
    def score_display(self):
        if self.game_state==GameState.IS_PLAYING:
            self.display_level()
            score = Score()
            score_surface = score.get_score(score=int(self.score))
            pos_x = 288
            for surf in score_surface:
                self.screen.blit(surf, surf.get_rect(center=(pos_x, 100)))
                pos_x += 15
        elif self.game_state == GameState.IS_GAME_OVER or  self.game_state == GameState.IS_PAUSE:

            self.save.update_scores((int(self.score),int(self.high_score)))
            score_surface = self.game_font.render(f'Last Score = {str(int(self.score))} ', True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(288, 200))
            self.screen.blit(score_surface, score_rect)

            high_score_surface = self.game_font.render(f'High Score = {str(int(self.high_score))} ', True,
                                                       (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(288, 850))
            self.screen.blit(high_score_surface, high_score_rect)

    def create_pipe(self) -> tuple:
        pipe_pos = random.choice(self.pipe_height)
        bottom_pipe = self.pipe.image.get_rect(midtop=(self.pipe_starting_pos_x, pipe_pos))
        top_pipe = self.pipe.image.get_rect(midbottom=(self.pipe_starting_pos_x, pipe_pos - self.pipe_spacing))
        return bottom_pipe, top_pipe

    def move_pipes(self) -> list[pygame.Rect]:
        for pipe in self.pipes:
            pipe.centerx -= 5
        visibles_pipes = [pipe for pipe in self.pipes if pipe.right > -50]
        return visibles_pipes

    def draw_pipes(self):
        for pipe in self.pipes:
            if pipe.bottom >= self.screen_height:
                self.screen.blit(self.pipe.image, pipe)
            else:
                flip_pip = pygame.transform.flip(self.pipe.image, False, True)
                self.screen.blit(flip_pip, pipe)

    def check_collision(self) -> GameState:
        for pipe in self.pipes:
            if self.bird.sprite.rect.colliderect(pipe):
                self.sounds_manager.play(Sounds.DEATH)
                return GameState.IS_GAME_OVER
        if self.bird.sprite.rect.top <= -100 or self.bird.sprite.rect.bottom >= 900:
            return GameState.IS_GAME_OVER
        return GameState.IS_PLAYING

    def remake_game(self):
        self.bird.sprite.bird_movement = 0
        self.game_state = GameState.IS_PLAYING
        self.pipes.clear()
        self.bird.sprite.rect = self.bird.sprite.center_bird_rect()
        self.score = 0

    def spawn_pipes(self):
        self.pipes.extend(self.create_pipe())



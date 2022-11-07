import pygame, random, sys, os
from Bird import Bird
from Floor import Floor
from Pipe import Pipe
from Sounds import SoundManager
from Enumeration import *
from Save import Save
from Score import Score
from Level import Level

os.environ['SDL_MOUSE_TOUCH_EVENTS'] = '1'


class Game():
    def __init__(self):

        pygame.init()
        info = pygame.display.Info()
        w = info.current_w
        h = info.current_h

       # print(f"default screen_width {500} and screen_height {1000} ratio= {500 / 1000},my screnn width {w} and height {h} and ratio = {w / h}")
        self.render_surface(w, h)
        self.game_font: pygame.font.Font = pygame.font.Font("assets/font/Pixeled.ttf", 20)
        self.game_state: GameState = GameState.IS_PAUSE
        self.init_levels()
        self.init_surface_vars()
        self.sounds_manager: SoundManager = SoundManager()
        self.SPAWN_PIPE = pygame.USEREVENT
        self.BIRDFLAP = pygame.USEREVENT + 1
        pygame.time.set_timer(self.SPAWN_PIPE, self.current_level.SPAWN_PIPE_TIME)
        pygame.time.set_timer(self.BIRDFLAP, self.current_level.BIRD_FLAP_TIME)
        self.clock = pygame.time.Clock()
        self.frame_rate = 120
        self.display_surface()

    def init_levels(self):
        self.current_level_int: int = 1
        self.levels: list[Level] = [
            Level("Level 1", 20, GameBackground.DAY, BirdColor.BLUE, PipeColor.GREEN),
            Level("Level 2", 40, GameBackground.DAY, BirdColor.BLUE, PipeColor.RED),
            Level("Level 3", 80, GameBackground.DAY, BirdColor.BLUE, PipeColor.GREEN),
            Level("Level 4", 100, GameBackground.NIGHT, BirdColor.RED, PipeColor.GREEN),
            Level("Level 5", 120, GameBackground.DAY, BirdColor.YELLOW, PipeColor.RED),
            Level("Level 6", 140, GameBackground.NIGHT, BirdColor.RED, PipeColor.RED),
        ]
        self.current_level: Level = self.levels[self.current_level_int - 1]

    def init_surface_vars(self):
        self.bird_sprite: Bird = Bird(self.screen, self.current_level.bird_frames)
        self.bg: pygame.Surface = self.current_level.BG
        self.pipe_height: list[int] = self.current_level.PIPE_HEIGHT_LIST
        self.pipe_spacing: int = self.current_level.PIPE_SPACING

        self.bird: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle(self.bird_sprite)

        self.game_starting: pygame.Surface = pygame.transform.scale(
            pygame.image.load('assets/images/message.png').convert_alpha(),
            (self.screen.get_width() / 2, self.screen.get_height() / 2))

        self.game_over = pygame.transform.scale2x(
            pygame.image.load('assets/images/gameover.png').convert_alpha())
        self.game_over_rect: pygame.Rect = self.game_over.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.game_starting_rect: pygame.Rect = self.game_starting.get_rect(
            center=(self.screen.get_width() / 2, self.screen.get_height() / 2))
        self.floor: Floor = Floor(self.screen)
        self.save: Save = Save()
        self.score: int = self.save.get_data(SaveData.SCORE)
        self.high_score: int = self.save.get_data(SaveData.HIGH_SCORE)
        self.pipe_speed: int = 5
        self.pipe: Pipe = self.current_level.pipe
        self.pipes: list[pygame.Rect] = []

        self.pipe_starting_pos_x: int = self.screen.get_height() - 300  # 700
        self.score_sound_countdown: int = 200

    def display_fps(self):

        caption = "Hello {} {}- FPS:({:.0f}/{}) and screen info ({},{})".format(os.getlogin(),"Flappy Bird", self.clock.get_fps(), self.frame_rate,
                                                                     self.screen.get_width(), self.screen.get_height())
        pygame.display.set_caption(caption)

    def render_surface(self, screen_width: int = 500, screen_height: int = 1000):
        # int((h - 50) * 0.5625), h - 50
        if screen_height < screen_width:
            w: int = int((screen_height - 50) * 0.5625)
            h: int = int(screen_height - 50)
        else:
            if (screen_width / screen_height <= 0.6):
                w: int = screen_width
                h: int = screen_height
            else:
                w: int = int((screen_height - 50) * 0.5625)
                h: int = int(screen_height - 50)
        self.screen = pygame.display.set_mode((w, h), pygame.SCALED | pygame.RESIZABLE)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save.save_data()
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                #pygame.display._resize_event(event)
                self.render_surface(event.w, event.h)
                pygame.display.update()
                # self.display_surface()
            # if event.type == pygame.KEYDOWN and event.type == pygame.KEYUP: game.game_state = GameState.IS_PAUSE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.onclick()
            if event.type == pygame.FINGERDOWN:
                self.onclick()
            if event.type == self.SPAWN_PIPE:
                self.spawn_pipes()
            if event.type == self.BIRDFLAP:
                self.bird.sprite.on_event_bird_flap()
        # return True

    def onclick(self):
        if self.game_state == GameState.IS_PLAYING:
            self.bird.sprite.update_movement()
            self.sounds_manager.play(Sounds.FLAP)
        elif self.game_state == GameState.IS_GAME_OVER or self.game_state == GameState.IS_PAUSE:
            self.remake_game()

    def display_surface(self):
        # screen = pygame.display.get_surface()
        #print(self.pipe_height)
        going = True
        while going:
            self.handle_events()
            self.screen.blit(self.bg, (0, 0))
            if self.game_state == GameState.IS_PLAYING:
                self.run()
            elif self.game_state == GameState.IS_GAME_OVER:
                self.update_screen_on_over_game()
            elif self.game_state == GameState.IS_PAUSE:
                self.update_screen_on_pause_game()
            elif self.game_state == GameState.IS_END_LEVEl_AND_GO_TO_NEXT_LEVEL:
                self.update_screen_on_start_new_level()
                pygame.time.set_timer(self.BIRDFLAP, self.current_level.BIRD_FLAP_TIME)
                pygame.time.set_timer(self.SPAWN_PIPE, self.current_level.SPAWN_PIPE_TIME)
                self.screen.blit(self.bg, (0, 0))

            self.update_floor_position()
            # pygame.display.update()
            self.display_fps()
            pygame.display.flip()
            self.clock.tick(self.frame_rate)

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
        if self.floor.position_x <= -self.screen.get_width():
            self.floor.position_x = 0

    def update_score(self) -> tuple:
        self.score += 0.01
        if self.score > self.high_score:
            self.high_score = self.score
        if self.score >= self.current_level.high_score and self.current_level_int < len(self.levels):
            self.current_level_int += 1
            self.game_state = GameState.IS_END_LEVEl_AND_GO_TO_NEXT_LEVEL
            #print(self.current_level_int)

        return self.score, self.high_score

    def display_level(self):
        level_surface = self.game_font.render(self.current_level.name, True, (255, 255, 255))
        level_rect = level_surface.get_rect(center=(self.screen.get_width() / 2, 50))
        self.screen.blit(level_surface, level_rect)

    def score_display(self):
        if self.game_state == GameState.IS_PLAYING:
            self.display_level()
            score = Score()
            score_surface = score.get_score(score=int(self.score))
            pos_x = self.screen.get_width() / 2
            for surf in score_surface:
                self.screen.blit(surf, surf.get_rect(center=(pos_x, 100)))
                pos_x += 15
        elif self.game_state == GameState.IS_GAME_OVER or self.game_state == GameState.IS_PAUSE:

            self.save.update_scores((int(self.score), int(self.high_score)))
            score_surface = self.game_font.render(f'Last Score = {str(int(self.score))} ', True, (255, 255, 255))
            score_rect = score_surface.get_rect(center=(self.screen.get_width() / 2, 200))
            self.screen.blit(score_surface, score_rect)

            high_score_surface = self.game_font.render(f'High Score = {str(int(self.high_score))} ', True,
                                                       (255, 255, 255))
            high_score_rect = high_score_surface.get_rect(center=(self.screen.get_width() / 2, 850))
            self.screen.blit(high_score_surface, high_score_rect)

    def create_pipe(self) -> tuple:
        pipe_pos = random.choice(self.pipe_height)
        #print(pipe_pos)
        bottom_pipe = self.pipe.image.get_rect(midtop=(self.pipe_starting_pos_x, pipe_pos))
        top_pipe = self.pipe.image.get_rect(midbottom=(self.pipe_starting_pos_x, pipe_pos - self.pipe_spacing))
        return bottom_pipe, top_pipe

    def move_pipes(self) -> list[pygame.Rect]:
        for pipe in self.pipes:
            # pass
            pipe.centerx -= self.pipe_speed
        visibles_pipes = [pipe for pipe in self.pipes if pipe.right > -50]
        self.pipes = visibles_pipes
        return visibles_pipes

    def draw_pipes(self):
        for pipe in self.pipes:
            if pipe.bottom >= self.screen.get_height():
                self.screen.blit(self.pipe.image, pipe)
            else:
                flip_pip = pygame.transform.flip(self.pipe.image, False, True)
                self.screen.blit(flip_pip, pipe)

    def remake_game(self):
        self.bird.sprite.bird_movement = 0
        self.game_state = GameState.IS_PLAYING
        self.pipes.clear()
        self.bird.sprite.rect = self.bird.sprite.center_bird_rect()
        self.score:int = 0

    def spawn_pipes(self):
        self.pipes.extend(self.create_pipe())

    def check_collision(self) -> GameState:
        for pipe in self.pipes:
            if self.bird.sprite.rect.colliderect(pipe):
                self.sounds_manager.play(Sounds.DEATH)
                return GameState.IS_GAME_OVER
        if self.bird.sprite.rect.top <= 0 or self.bird.sprite.rect.bottom >= self.screen.get_height() - 100:
            self.sounds_manager.play(Sounds.DEATH)
            return GameState.IS_GAME_OVER
        return GameState.IS_PLAYING


if __name__ == '__main__':
    game = Game()

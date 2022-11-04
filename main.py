import pygame, sys, os

from Game import Game
from Enumeration import *
from Level import Level
import random
os.environ['SDL_MOUSE_TOUCH_EVENTS'] = '1'


def onclick(game: Game):
    if game.game_state==GameState.IS_PLAYING:
        game.bird.sprite.update_movement()
        game.sounds_manager.play(Sounds.FLAP)
    elif game.game_state ==GameState.IS_GAME_OVER or  game.game_state == GameState.IS_PAUSE:
        game.remake_game()


def main():
    pygame.init()
    frame_rate = 120
    screen_width = 576
    screen_height = 1024
    screen = pygame.display.set_mode((screen_width, screen_height))
    game = Game(screen,[
        Level("Level 1",40, GameBackground.DAY, BirdColor.BLUE, PipeColor.GREEN),
        Level("Level 2", 80, GameBackground.DAY, BirdColor.BLUE, PipeColor.RED),
        Level("Level 3", 100, GameBackground.DAY, BirdColor.BLUE, PipeColor.GREEN),
        Level("Level 4", 120, GameBackground.NIGHT, BirdColor.RED, PipeColor.GREEN),
        Level("Level 5", 150, GameBackground.DAY, BirdColor.YELLOW, PipeColor.RED),
        Level("Level 6", 160, GameBackground.NIGHT, BirdColor.RED, PipeColor.RED),
    ])
    frame_rate = game.save.get_data(SaveData.FRAME_RATE)
    BIRDFLAP = pygame.USEREVENT + 1
    pygame.time.set_timer(BIRDFLAP, game.current_level.BIRD_FLAP_TIME)
    SPAWN_PIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWN_PIPE, game.current_level.SPAWN_PIPE_TIME)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.save.save_data()
                pygame.quit()
                sys.exit()
            #if event.type == pygame.KEYDOWN and event.type == pygame.KEYUP: game.game_state = GameState.IS_PAUSE
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                onclick(game)
            if event.type == pygame.FINGERDOWN:
                onclick(game)
            if event.type == SPAWN_PIPE:
                game.spawn_pipes()
            if event.type == BIRDFLAP:
                game.bird.sprite.on_event_bird_flap()
        game.screen.blit(game.bg, (0, 0))
        if game.game_state==GameState.IS_PLAYING:
            game.run()
        elif game.game_state == GameState.IS_GAME_OVER:
            game.update_screen_on_over_game()
        elif game.game_state == GameState.IS_PAUSE:
            game.update_screen_on_pause_game()
        elif game.game_state == GameState.IS_END_LEVEl_AND_GO_TO_NEXT_LEVEL:
            game.update_screen_on_start_new_level()
            pygame.time.set_timer(BIRDFLAP, game.current_level.BIRD_FLAP_TIME)
            pygame.time.set_timer(SPAWN_PIPE, game.current_level.SPAWN_PIPE_TIME)
            game.screen.blit(game.bg, (0, 0))

        game.update_floor_position()
        pygame.display.update()
        clock.tick(frame_rate)


if __name__ == '__main__':
    main()

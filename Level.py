from typing import Type

import pygame
from Enumeration import *
from Pipe import Pipe


class Level():
    def __init__(self, name: str,
                 high_score:int,
                 bg_color: GameBackground,
                 bird_color: BirdColor,
                 pipe_color: PipeColor,
                 pipe_height_list=None,
                 bird_flap_time: int = 200, spawn_pipe_time: int = 1200,
                 pipe_spacing: int = 300):
        self.name = name
        self.high_score = high_score
        if pipe_height_list is None:
            pipe_height_list = [400, 600, 800]
        self.BG: pygame.Surface = self.get_bg_surface(bg_color)
        self.BIRD_FLAP_TIME: int = bird_flap_time
        self.SPAWN_PIPE_TIME: int = spawn_pipe_time
        self.PIPE_SPACING: int = pipe_spacing
        self.PIPE_HEIGHT_LIST: list[int] = pipe_height_list
        self.bird_frames: list[pygame.Surface] = self.get_bird_frames(bird_color)
        self.pipe: Pipe = self.get_pipe(pipe_color)

    def get_bg_surface(self, bg: GameBackground) -> pygame.Surface:
        if bg == GameBackground.DAY:
            return pygame.transform.scale2x(pygame.image.load('assets/images/bg/background-day.png').convert_alpha())
        elif bg == GameBackground.NIGHT:
            return pygame.transform.scale2x(pygame.image.load('assets/images/bg/background-night.png').convert_alpha())

    def get_bird_frames(self, color: BirdColor) -> list[pygame.Surface]:
        if color == BirdColor.BLUE:
            return [
                pygame.transform.scale2x(pygame.image.load(
                    'assets/images/bird/blue/bluebird-downflap.png').convert_alpha()),
                pygame.transform.scale2x(pygame.image.load(
                    'assets/images/bird/blue/bluebird-midflap.png').convert_alpha()),
                pygame.transform.scale2x(pygame.image.load(
                    'assets/images/bird/blue/bluebird-upflap.png').convert_alpha())
            ]
        elif color == BirdColor.YELLOW:
            return [
                pygame.transform.scale2x(pygame.image.load(
                    'assets/images/bird/yellow/yellowbird-downflap.png').convert_alpha()),
                pygame.transform.scale2x(pygame.image.load(
                    'assets/images/bird/yellow/yellowbird-midflap.png').convert_alpha()),
                pygame.transform.scale2x(pygame.image.load(
                    'assets/images/bird/yellow/yellowbird-upflap.png').convert_alpha())
            ]
        elif color == BirdColor.RED:
            return [
                pygame.transform.scale2x(pygame.image.load(
                    'assets/images/bird/red/redbird-downflap.png').convert_alpha()),
                pygame.transform.scale2x(pygame.image.load(
                    'assets/images/bird/red/redbird-midflap.png').convert_alpha()),
                pygame.transform.scale2x(pygame.image.load(
                    'assets/images/bird/red/redbird-upflap.png').convert_alpha())
            ]

    def get_pipe(self, pipe_color: PipeColor) -> Pipe:
        return Pipe(pipe_color)

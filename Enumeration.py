from enum import Enum


class Sounds(Enum):
    FLAP = 1
    DEATH = 2
    SCORE = 3
class SaveData(Enum):

    HIGH_SCORE = 1
    SCORE = 2
    SCREEN_HEIGHT =3
    SCREEN_WIDTH = 4
    FRAME_RATE = 5

class GameBackground(Enum):
    NIGHT = 1
    DAY =2
class BirdColor(Enum):
    BLUE = 1
    RED = 2
    YELLOW =3
class PipeColor(Enum):
    GREEN = 1
    RED = 2

class GameState(Enum):
    IS_PLAYING =1
    IS_GAME_OVER = 2
    IS_END_LEVEl_AND_GO_TO_NEXT_LEVEL = 3
    IS_PAUSE = 4

import pygame
from Enumeration import Sounds

class SoundManager:

    def __init__(self):
        self.sounds = {
            Sounds.FLAP: pygame.mixer.Sound("assets/audio/wing.wav"),
            Sounds.DEATH: pygame.mixer.Sound("assets/audio/hit.wav"),
            Sounds.SCORE: pygame.mixer.Sound("assets/audio/point.wav")
        }

    def play(self, name):
        self.sounds[name].play()

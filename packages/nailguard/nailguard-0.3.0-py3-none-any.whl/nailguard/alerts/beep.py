from pathlib import Path
from time import sleep

import pygame

from .base import Alert


class BeepAlert(Alert):
    
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        sound_path = str(Path(__file__).parent.parent / "assets" / "error.wav")
        self.sound = pygame.mixer.Sound(sound_path)
    
    def on_start(self):
        self.sound.play()
        sleep(0.5)
    
    def on_active(self):
        self.sound.play()
        sleep(0.5)

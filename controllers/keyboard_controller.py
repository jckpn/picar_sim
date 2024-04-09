import pygame
from controllers import PicarController


class KeyboardController(PicarController):
    def __init__(self):
        super().__init__()

    def get_controls(self, *args, **kwargs):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            throttle = 1.0
        else:
            throttle = 0.0

        if keys[pygame.K_LEFT]:
            steer = 0.0
        elif keys[pygame.K_RIGHT]:
            steer = 1.0
        else:
            steer = 0.5

        return throttle, steer

import pygame
from controllers import PicarController


class KeyboardController(PicarController):
    def __init__(self):
        super().__init__()

    def predict_from_state(self, *args):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            speed = 35
        else:
            speed = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            angle = 72
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            angle = 108
        else:
            angle = 90

        return angle, speed

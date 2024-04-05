import pygame
import numpy as np


class MouseController:
    def __init__(self, display_size=(1050, 600)):
        self.display_size = display_size

    def get_controls(self, *args):
        # get mouse pos
        mx, my = pygame.mouse.get_pos()

        mx -= self.display_size[0] / 2
        my -= self.display_size[1] / 2

        throttle = 1 if my < 0 else 0
        steer = np.clip((mx + 300) / 600, 0, 1)

        return throttle, steer

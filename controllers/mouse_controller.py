import pygame
import numpy as np


class MouseController:
    def get_controls(self, *args):
        mx, my = pygame.mouse.get_pos()
        dw, dh = pygame.display.get_surface().get_size()

        throttle = 1 if my < dh // 2 else 0
        throttle = np.clip(throttle, 0, 1)
        if throttle == 0:
            return 0, 0.5

        control_w = dw
        mx -= dw // 2 - control_w // 2
        steer = mx / control_w
        steer = np.clip(steer, 0, 1)

        return throttle, steer

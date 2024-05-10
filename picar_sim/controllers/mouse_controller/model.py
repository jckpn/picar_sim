import pygame
import numpy as np


class MouseController:
    def __init__(self, sensitivity=0.1):
        self.sensitivity = sensitivity
        
    def predict_from_state(self, *args):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        display_w, display_h = pygame.display.get_surface().get_size()
        picar_x = display_w // 2
        picar_y = display_h // 2

        speed = 35 if mouse_y < picar_y else 0
        angle = 90 + (mouse_x - picar_x) * self.sensitivity
        angle = np.clip(angle, 50, 130)
        return angle, speed

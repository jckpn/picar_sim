import pygame


class MouseController:
    def get_controls(self, *args):
        # get mouse pos
        mx, my = pygame.mouse.get_pos()

        # get display size
        w, h = pygame.display.get_surface().get_size()

        throttle = my / h
        steer = mx / w

        return throttle, steer

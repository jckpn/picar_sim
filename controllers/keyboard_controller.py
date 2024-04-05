import pygame


class KeyboardController:
    def get_controls(self, *args):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            throttle = 1
        else:
            throttle = 0

        if keys[pygame.K_LEFT]:
            steer = 0
        elif keys[pygame.K_RIGHT]:
            steer = 1
        else:
            steer = 0.5

        return throttle, steer

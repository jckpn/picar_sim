import pygame


class KeyboardController:
    def get_controls(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            throttle = 1

        if keys[pygame.K_LEFT]:
            steer = 0
        elif keys[pygame.K_RIGHT]:
            steer = 1

        return throttle, steer

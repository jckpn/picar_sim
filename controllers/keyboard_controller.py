import pygame


class KeyboardController:
    def get_controls(self, throttle=0, steer=0.5):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            throttle = 1

        if keys[pygame.K_LEFT]:
            steer = 0
        elif keys[pygame.K_RIGHT]:
            steer = 1

        return throttle, steer

import pygame


class KeyboardController:
    def predict(self, picar, env):
        angle, speed = 90, 0  # defaults

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            speed = 35
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            angle = 55
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            angle = 125

        return angle, speed

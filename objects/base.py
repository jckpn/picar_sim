import pygame
from utils import scale_coords, center_rotate


class SimulatorObject:
    def __init__(self, center, size, direction, image_path):
        self.center = center
        self.size = size
        self.direction = direction
        self.image = self.load_image(image_path, size)

    def load_image(self, path, size):
        image = pygame.image.load(path)
        image = pygame.transform.smoothscale(image, scale_coords(size))
        return image

    def update(self, delta_time):
        pass

    def render(self, display, perspective):
        win_center = (
            display.get_width() // 2,
            display.get_height() // 2,
        )
        
        angle = self.direction - perspective.direction

        pivot = scale_coords(self.center)
        pivot = (
            pivot[0] + win_center[0],
            pivot[1] + win_center[1],
        )

        offset = scale_coords(
            (
                -perspective.center[0],
                -perspective.center[1],
            )
        )

        blit_image, blit_rect = center_rotate(
            self.image, angle, pivot, pygame.math.Vector2(offset)
        )

        display.blit(blit_image, blit_rect)

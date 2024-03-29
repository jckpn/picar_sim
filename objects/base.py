import pygame
from utils import scale_coords


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
        rotated_image = pygame.transform.rotate(self.image, -angle)

        # proper implementation should work for any object, but I've spent too long trying
        # so here's a janky soliution that works for picar or tracks only
        if perspective.__class__.__name__ == "Picar":
            offset = pygame.math.Vector2(
                *scale_coords(
                    (
                        self.center[0] - perspective.center[0],
                        self.center[1] - perspective.center[1],
                    )
                )
            )
            pivot = pygame.math.Vector2(*win_center)
            rotated_offset = offset.rotate(angle)
            rect = rotated_image.get_rect(center=pivot + rotated_offset)
        else:
            pivot = scale_coords(self.center)
            pivot = (
                pivot[0] + win_center[0],
                pivot[1] + win_center[1],
            )
            rect = rotated_image.get_rect(center=pivot)

        display.blit(rotated_image, rect)

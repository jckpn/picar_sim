import pygame
from utils import scale_coords, rotate


class WoodBlock:
    def __init__(
        self,
        image_path,
        center_x=None,
        center_y=None,
        width=10,
        height=10,
        # orientation=0,  # probably not needed tbh
    ):
        self.center_x = center_x
        self.center_y = center_y
        self.width = width
        self.height = height

        self.IMAGE = self.load_pygame_image(image_path, self.WIDTH, self.HEIGHT)

    def load_pygame_image(self, path, width, height):
        image = pygame.image.load(path)
        scaled_coords = scale_coords(width, height)
        scaled_image = pygame.transform.smoothscale(image, scaled_coords)

        return scaled_image

    def render(self, display, perspective=None):
        if perspective is None:
            scaled_coords = scale_coords(self.center_x, self.center_y)
            rect = self.IMAGE.get_rect(center=scaled_coords)
            rotated_img = self.IMAGE
        else:
            # picar perspective

            rotated_img, rect = rotate(
                self.IMAGE,
                -perspective.direction,
                pygame.math.Vector2(
                    scale_coords(perspective.display_x, perspective.display_y)
                ),
                pygame.math.Vector2(
                    scale_coords(
                        -perspective.center_x + self.center_x,
                        -perspective.center_y + self.center_y,
                    )
                ),
            )

        display.blit(rotated_img, rect)

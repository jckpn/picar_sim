import pygame
from functions import scale_coords, rotate


class Track:
    """
    Represents a track in the simulator.

    Args:
        env (Environment): The environment object.
        track_name (str): The name of the track.
        width (int, optional): The width of the track image. Defaults to 300.
        height (int, optional): The height of the track image. Defaults to 164.
    """

    def __init__(self, image_path, width=300, height=164, center_x=0, center_y=0):
        self.WIDTH = width
        self.HEIGHT = height
        self.center_x = center_x
        self.center_y = center_y

        self.IMAGE = self.load_pygame_image(image_path, self.WIDTH, self.HEIGHT)

    def load_pygame_image(self, path, width, height):
        image = pygame.image.load(path)
        scaled_coords = scale_coords(width, height)
        scaled_image = pygame.transform.smoothscale(image, scaled_coords)

        return scaled_image

    def render(self, display, perspective=None):
        """
        Renders the track on the display.

        Args:
            display (pygame.Surface): The surface to render the track on.
            perspective (Perspective, optional): The perspective object. Defaults to None.
        """
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

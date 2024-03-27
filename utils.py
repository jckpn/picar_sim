import pygame
from constants import DISPLAY_SCALE
import numpy as np
import cv2


# https://stackoverflow.com/a/49413006
# rotate center around arbitrary point -- needed for perspective shifts
def center_rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotate(surface, -angle)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot + rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.


def check_collisions(picar, obstacles):
    for obstacle in obstacles:
        if picar.rect.colliderect(obstacle.rect):
            return True
    return False


def scale_coords(tuple):
    return (tuple[0] * DISPLAY_SCALE, tuple[1] * DISPLAY_SCALE)


def get_picar_view(display, picar):
    view_size = 32
    y_offset = -28  # to get picar out of view

    view_rect = (
        picar.display_x - view_size // 2,
        picar.display_y - view_size // 2 + y_offset,
        view_size,
        view_size,
    )
    view_rect = scale_coords(*view_rect)
    view_surface = display.subsurface(view_rect).copy()

    # convert to cv2 image
    view_img = pygame.surfarray.array3d(view_surface)
    view_img = np.rot90(view_img)
    view_img = cv2.flip(view_img, 0)
    view_img = cv2.cvtColor(view_img, cv2.COLOR_RGB2BGR)

    return view_img

import pygame
from constants import DISPLAY_SCALE
import numpy as np
import cv2



def check_collisions(picar, obstacles):
    for obstacle in obstacles:
        if picar.rect.colliderect(obstacle.rect):
            return True
    return False


def scale_coords(tuple):
    return (tuple[0] * DISPLAY_SCALE, tuple[1] * DISPLAY_SCALE)


def get_picar_view(display, view_size=32, y_offset=-27):
    view_rect = (
        display.get_width() // 2 - view_size * DISPLAY_SCALE // 2,
        display.get_height() // 2
        - view_size * DISPLAY_SCALE // 2
        + y_offset * DISPLAY_SCALE,
        view_size * DISPLAY_SCALE,
        view_size * DISPLAY_SCALE,
    )
    view_surface = display.subsurface(view_rect).copy()

    # convert to cv2 image
    view_img = pygame.surfarray.array3d(view_surface)
    view_img = np.rot90(view_img)
    view_img = cv2.flip(view_img, 0)
    view_img = cv2.cvtColor(view_img, cv2.COLOR_RGB2BGR)

    return view_img

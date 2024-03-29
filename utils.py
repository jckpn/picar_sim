import pygame
import numpy as np
import cv2


def scale_coords(coords, scale=4):
    return coords * scale if isinstance(coords, int) else [scale * c for c in coords]


def get_picar_view(display, view_size=(40, 40)):
    view_size = scale_coords(view_size)
    y_offset = scale_coords(10)

    view_rect = (
        display.get_width() // 2 - view_size[1] // 2,
        display.get_height() // 2 - y_offset - view_size[0],
        *view_size,
    )

    # capture rect and convert to cv2 image
    view_cap = display.subsurface(view_rect).copy()
    view_cap = pygame.surfarray.array3d(view_cap)
    view_cap = np.rot90(view_cap)
    view_cap = cv2.flip(view_cap, 0)
    view_cap = cv2.cvtColor(view_cap, cv2.COLOR_RGB2BGR)

    # show view
    cv2.imshow("view", view_cap)
    # pygame.draw.rect(display, (255, 0, 255), view_rect, 2)

    return view_cap

import pygame
import numpy as np
from scaler import scale_coords


class SimulatorObject:  # TODO: inherit pygame sprite class?
    def __init__(
        self,
        center,
        size,
        direction=0,
        image_path=None,
        color=(0, 0, 0),
        can_collide=False,
    ):
        self.center = np.array(center, dtype=float)
        self.size = np.array(size, dtype=int)
        self.direction = direction
        self.can_collide = can_collide
        self.image_path = image_path
        self.image = None
        self.color = color

        if image_path:
            self.image = pygame.transform.smoothscale(
                pygame.image.load(image_path), scale_coords(size)
            )

    def update(self, dt, env):
        pass

    def render(self, display, perspective):
        # the proper implementation should work for any object, but I've spent too long
        # trying so here's a janky solution that just follows picar or does nothing

        direction = (
            self.direction - perspective.direction if perspective else self.direction
        )

        if perspective.__class__.__name__ == "Picar":
            blit_pos = scale_coords((
                    self.center[0] - perspective.center[0],
                    self.center[1] - perspective.center[1],
                ))  # fmt: off
            blit_pos = pygame.math.Vector2(blit_pos).rotate(direction)
        else:
            blit_pos = scale_coords(self.center)

        # apply offset so (0, 0) is center of display
        offset = (display.get_width() // 2, display.get_height() // 2)
        blit_pos += offset

        if self.image:
            image = pygame.transform.rotate(self.image, -direction)
            rect = image.get_rect(center=blit_pos)
            display.blit(image, rect)
        else:
            pygame.draw.circle(
                display, self.color, blit_pos, scale_coords(self.size[0] // 2)
            )

import pygame
import numpy as np
from scaler import scale_coords


class SimulatorObject:  # TODO: inherit pygame sprite class?
    def __init__(
        self,
        center,
        size,
        angle,
        image_path=None,
        color=(0, 0, 0),
        can_collide=False,
    ):
        self.center = np.array(center, dtype=float)
        self.size = np.array(size, dtype=int)
        self.angle = angle
        self.can_collide = can_collide
        self.image_path = image_path

        if image_path:
            self.image = pygame.transform.smoothscale(
                pygame.image.load(image_path), scale_coords(size)
            )
        else:
            # if no image, use a rectangle
            self.image = pygame.Surface(size=scale_coords(self.size))  # type: ignore
            self.image.fill(color)

    def update(self, dt, env):
        pass

    def render(self, display, perspective):
        # the proper implementation should work for any object, but I've spent too long
        # trying so here's a janky solution that just follows picar or does nothing
        
        angle = self.angle - perspective.angle if perspective else self.angle
        image = pygame.transform.rotate(self.image, -angle)
        
        if perspective.__class__.__name__ == "Picar":
            offset = scale_coords(
                (
                    self.center[0] - perspective.center[0],
                    self.center[1] - perspective.center[1],
                )
            )
            offset = pygame.math.Vector2(offset).rotate(angle)
        else:
            offset = scale_coords(self.center)

        rect = image.get_rect(center=offset)

        # apply offset so (0, 0) is center of display
        rect = rect.move((display.get_width() // 2, display.get_height() // 2))

        display.blit(image, rect)

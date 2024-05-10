import pygame
import numpy as np


class SimulatorObject:  # TODO: inherit pygame sprite class?
    def __init__(
        self,
        sim,
        center=(0, 0),
        size=(20, 20),
        direction=0,
        image_path=None,
        can_collide=False,
    ):
        self.sim = sim
        self.center = np.array(center, dtype=float)
        self.size = np.array(size, dtype=int)
        self.direction = direction
        self.can_collide = can_collide
        self.image_path = image_path
        self.image = self.load_image(image_path, size)

    def load_image(self, image_path, size):
        self.image = pygame.transform.smoothscale(
            pygame.image.load(image_path), self.sim.scale_coords(size)
        )

    def update(self, dt, env):
        pass

    def get_relative_position(self, perspective, display):
        direction = (
            self.direction - perspective.direction if perspective else self.direction
        )

        if perspective.__class__.__name__ == "Picar":
            position = self.sim.scale_coords((
                    self.center[0] - perspective.center[0],
                    self.center[1] - perspective.center[1],
                ))  # fmt: off
            position = pygame.math.Vector2(position).rotate(direction)
        else:
            position = self.sim.scale_coords(self.center)

        # apply offset so (0, 0) is center of display
        position += (display.get_width() // 2, display.get_height() // 2)

        return position, direction

    def render(self, display, perspective):
        # the proper implementation should work for any object, but I've spent too long
        # trying so here's a janky solution that works for the picar

        blit_pos, direction = self.get_relative_pos(perspective, display)

        if self.image:
            image = pygame.transform.rotate(self.image, -direction)
            rect = image.get_rect(center=blit_pos)
            display.blit(image, rect)

            # add class name as text
            font = pygame.font.Font(None, 20)
            text = font.render(self.__class__.__name__, True, self.color)
            display.blit(text, blit_pos + (5, 5))

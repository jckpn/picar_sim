import pygame
from utils import scale_coords
import numpy as np


class Picar:
    def __init__(
        self,
        image_path,
        start_center_x=60,
        start_center_y=60,
        display_x=60,
        display_y=60,
    ):
        self.WIDTH = 15  # cm
        self.HEIGHT = 25
        self.MAX_VELOCITY = 20  # cm/s
        self.MAX_ACCELERATION = 20  # cm/s/s
        self.MAX_STEERING_ANGLE = 4  # degrees??
        self.STEERING_SMOOTHING = 0.5  # higher value => longer to reach target angle

        self.center_x = start_center_x
        self.center_y = start_center_y
        self.display_x = display_x
        self.display_y = display_y
        self.velocity = 0
        self.acceleration = 0
        self.direction = 0  # degrees
        self.throttle = 0
        self.steer = 0
        self.steering_angle = 0

        self.IMAGE = self.load_pygame_image(image_path, self.WIDTH, self.HEIGHT)

    def load_pygame_image(self, path, width, height):
        image = pygame.image.load(path)
        scaled_coords = scale_coords(width, height)
        scaled_image = pygame.transform.smoothscale(image, scaled_coords)

        return scaled_image

    def update(self, delta_time):
        target_steering_angle = (self.steer * 2 - 1) * self.MAX_STEERING_ANGLE
        a = self.STEERING_SMOOTHING ** (delta_time * 10)
        self.steering_angle = a * self.steering_angle + (1 - a) * target_steering_angle
        self.direction += self.steering_angle * self.velocity * delta_time

        self.acceleration = (self.throttle * 2 - 1) * self.MAX_ACCELERATION
        self.velocity += self.acceleration * delta_time
        self.velocity = np.clip(self.velocity, 0, self.MAX_VELOCITY)
        velocity_x = self.velocity * np.sin(np.radians(self.direction))
        velocity_y = self.velocity * -np.cos(np.radians(self.direction))
        self.center_x += velocity_x * delta_time
        self.center_y += velocity_y * delta_time

    def render(self, display, perspective=None):
        if perspective is None:
            scaled_coords = scale_coords(self.center_x, self.center_y)
            img_rotated = pygame.transform.rotozoom(  # use rotozoom to force AA
                self.IMAGE, -self.direction, 1.0
            )
            rect = img_rotated.get_rect(center=scaled_coords)
        else:
            # picar perspective
            scaled_coords = scale_coords(self.display_x, self.display_y)
            rect = self.IMAGE.get_rect(center=scaled_coords)
            img_rotated = self.IMAGE

        display.blit(img_rotated, rect)

    def render_extras(self, display):  # render as arrows
        self.render_extra(
            display,
            label="Throttle",
            row=0,
            val=self.throttle,
            min_val=0,
            max_val=1,
        )

        self.render_extra(
            display,
            label="Velocity",
            row=1,
            val=self.velocity,
            min_val=0,
            max_val=self.MAX_VELOCITY,
        )

        self.render_extra(
            display,
            label="Wheel Direction",
            row=2,
            val=self.steering_angle,
            min_val=-self.MAX_STEERING_ANGLE,
            max_val=self.MAX_STEERING_ANGLE,
        )

    def render_extra(self, display, label, row, val, min_val, max_val, size=200):
        range = max_val - min_val
        frac = (val - min_val) / range

        x = 10
        y = 10 + 30 * row

        pygame.draw.rect(
            display,
            (0, 0, 0),
            pygame.Rect(x, y, frac * size, 22),
        )

        pygame.draw.rect(
            display,
            (0, 0, 0),
            pygame.Rect(
                x,
                y,
                size,
                22,
            ),
            2,
        )

        font = pygame.font.Font(None, 21)
        text = font.render(f"{label}: {val:.1f}", True, (128, 128, 128))
        display.blit(text, (x + 6, y + 4))

    def set_controls(self, throttle, steer):
        assert 0 <= throttle <= 1
        assert 0 <= steer <= 1

        self.throttle = throttle
        self.steer = steer

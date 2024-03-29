from objects.base import SimObject
import numpy as np
import pygame
import cv2
from utils import scale_coords


class Picar(SimObject):
    def __init__(
        self,
        center=(0, 0),
        size=(17, 34),
        angle=0,
        image_path="objects/assets/picar.png",
        can_collide=True,
    ):
        super().__init__(center, size, angle, image_path, can_collide)

        # controls
        self.controls = {
            "throttle": 0.0,
            "steer": 0.0,
        }

        self.steering_thing = 2  # ??

        self.speed = 0.0
        self.max_speed = 20.0  # cm/s

        self.accel = 0.0
        self.max_accel = 20.0  # cm/s^2
        self.friction = 1

    def update(self, delta_time):
        # update direction
        self.angle += (
            (self.controls["steer"] * 2 - 1)
            * self.steering_thing
            * self.speed
            * delta_time
        )

        # update acceleration
        self.accel = (
            self.controls["throttle"] * self.max_accel - self.friction * self.speed
        )
        self.accel = np.clip(self.accel, -np.inf, self.max_accel)

        # update speed and velocity
        self.speed += self.accel * delta_time
        self.speed = np.clip(self.speed, -self.max_speed, self.max_speed)
        self.velocity = self.speed * np.array(
            [np.sin(np.radians(self.angle)), -np.cos(np.radians(self.angle))]
        )

        # update position
        self.center += self.velocity * delta_time

    def set_controls(self, throttle, steer):
        assert 0 <= throttle <= 1
        assert 0 <= steer <= 1

        self.controls["throttle"] = throttle
        self.controls["steer"] = steer

    def check_for_collisions(self, environment):
        if not self.can_collide:
            return

        for obj in environment:
            if not obj.can_collide or obj == self:
                continue

            distance = (
                np.linalg.norm(np.array(self.center) - np.array(obj.center))
                - np.mean(obj.size) / 2
                - np.mean(self.size) / 2
            )

            if distance < 0:
                return True

        return False

    def get_view(self, display, view_size=40):
        view_size = scale_coords(view_size)
        y_offset = scale_coords(10)

        view_rect = (
            display.get_width() // 2 - view_size // 2,
            display.get_height() // 2 - y_offset - view_size,
            view_size,
            view_size,
        )

        # capture rect and convert to cv2 image
        view_cap = display.subsurface(view_rect).copy()
        view_cap = pygame.surfarray.array3d(view_cap)
        view_cap = np.rot90(view_cap)
        view_cap = cv2.flip(view_cap, 0)
        view_cap = cv2.cvtColor(view_cap, cv2.COLOR_RGB2BGR)

        # show view
        # cv2.imshow("view", view_cap)
        pygame.draw.rect(display, (255, 0, 255), view_rect, 2)

        return view_cap

    def get_state(self, display):
        view = self.get_view(display)
        
        view = cv2.erode(view, kernel=np.ones((3, 3)), iterations=2)
        view = cv2.resize(view, (32, 32), interpolation=cv2.INTER_NEAREST)
        view = cv2.resize(view, (200, 200), interpolation=cv2.INTER_NEAREST)
        
        cv2.imshow("view", view)

        # # convert to grayscale
        # view = cv2.cvtColor(view, cv2.COLOR_BGR2GRAY)

        # # state idea: distance to nearest obstacle in each direction
        # view = cv2.erode(view, kernel=np.ones((5, 5)), iterations=1)
        # view = cv2.resize(view, (10, 10), interpolation=cv2.INTER_AREA)
        # state = [10 for _ in range(10)]

        # # scan each column from bottom to top
        # view = np.transpose(view)
        # view = np.flip(view, 0)
        # for col_idx, col in enumerate(view):
        #     for pixel_idx, pixel in enumerate(col):
        #         if pixel < 200:
        #             state[col_idx] = pixel_idx
        #             break

        # print(f"\n{state}\n")
        pass

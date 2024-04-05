from objects.base_object import BaseObject
import numpy as np


class Picar(BaseObject):
    def __init__(
        self,
        center=(0, 0),
        size=(17, 34),
        angle=0,
        image_path="objects/assets/picar.png",
        can_collide=True,
        smoothing=0.75,
    ):
        super().__init__(center, size, angle, image_path, can_collide)

        self.smoothing = smoothing

        # controls
        self.throttle = 0.0
        self.steer = 0.5

        # physics
        self.steering_thing = 2  # ??
        self.speed = 0.0
        self.max_speed = 30.0  # cm/s
        self.accel = 0.0
        self.max_accel = 25.0  # cm/s^2
        self.friction = 10.0  # cm/s^2

    def update(self, delta_time):
        # update direction
        self.angle += (
            (self.steer * 2 - 1) * self.steering_thing * self.speed * delta_time
        )
        self.angle %= 360

        # update acceleration
        self.accel = self.throttle * self.max_accel - self.friction
        self.accel = np.clip(self.accel, -np.inf, self.max_accel)

        # update speed and velocity
        self.speed += self.accel * delta_time
        self.speed = np.clip(self.speed, 0, self.max_speed)
        self.velocity = self.speed * np.array(
            [np.sin(np.radians(self.angle)), -np.cos(np.radians(self.angle))]
        )

        # update position
        self.center += self.velocity * delta_time

    def set_controls(self, throttle, steer):
        assert 0 <= throttle <= 1
        assert 0 <= steer <= 1

        self.throttle = throttle

        # TODO: make smoothing time-based
        self.steer = steer * (1 - self.smoothing) + self.steer * self.smoothing

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

        # def get_state(self, display):
        #     view = get_picar_view(display, view_size=40)

        #     view = cv2.erode(view, kernel=np.ones((3, 3)), iterations=2)
        #     view = cv2.resize(view, (32, 32), interpolation=cv2.INTER_NEAREST)
        #     view = cv2.resize(view, (200, 200), interpolation=cv2.INTER_NEAREST)

        #     cv2.imshow("view", view)

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

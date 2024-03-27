from objects.base import SimulatorObject
import numpy as np


class Picar(SimulatorObject):
    def __init__(
        self,
        center=(0, 0),
        size=(15, 25),
        direction=0,
        image_path="assets/picar.png",
    ):
        super().__init__(center, size, direction, image_path)

        self.throttle = 0
        self.steer = 0

        self.velocity = 0
        self.accel = 0

        self.max_velocity = 20  # cm/s
        self.max_accel = 20  # cm/s^2
        self.max_steer = 2  # ??
        self.friction = 10  # natural decel rate,cm/s^2

    def update(self, delta_time):
        # update direction
        self.direction += (
            (self.steer * 2 - 1) * self.max_steer * self.velocity * delta_time
        )

        # update acceleration
        self.accel = self.throttle * self.max_accel - self.friction

        # update velocity
        self.velocity += self.accel * delta_time
        self.velocity = np.clip(self.velocity, 0, self.max_velocity)

        # update position
        velocity_vector = (
            self.velocity * np.sin(np.radians(self.direction)),
            self.velocity * -np.cos(np.radians(self.direction)),
        )
        self.center = (
            self.center[0] + velocity_vector[0] * delta_time,
            self.center[1] + velocity_vector[1] * delta_time,
        )

    def set_controls(self, new_throttle, new_steer):
        assert 0 <= new_throttle <= 1
        assert 0 <= new_steer <= 1

        self.throttle = new_throttle
        self.steer = new_steer

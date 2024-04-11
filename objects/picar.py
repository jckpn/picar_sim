from objects.base import SimulatorObject
import numpy as np
from controllers import PicarController, KeyboardController


class Picar(SimulatorObject):
    def __init__(
        self,
        controller: PicarController = KeyboardController(),
        center=(0, 0),
        size=(13, 26),
        angle=0,
        image_path="objects/assets/picar.png",
    ):
        super().__init__(center, size, angle, image_path, can_collide=True)

        self.controller = controller

        # variables set by controller each frame
        self.controller_throttle = 0.0
        self.controller_steer = 0.5
        self.throttle = 0.0
        self.steer = 0.0

        # dynamic variables
        self.speed = 0.0
        self.wheel_angle = 0.0

        # constants -- these are total guesses atm
        self.turning_radius = 15.0  # cm
        self.max_speed = 30.0  # cm/s I think?
        self.accel = 25.0  # cm/s^2
        self.breaking_accel = 50.0  # breaking has faster accel
        self.max_wheel_angle = 40  # degrees
        self.wheel_actuation_speed = 160.0  # 40 / time it takes to turn wheel 0 -> 40

    def update(self, dt, env):
        # get controls from controller
        throttle, steer = self.controller.get_controls(self, env)
        self.set_controls(throttle, steer)

        # controls -> physics
        new_wheel_angle = (self.controller_steer * 2 - 1) * self.max_wheel_angle
        if new_wheel_angle > self.wheel_angle:
            self.wheel_angle += self.wheel_actuation_speed * dt
            self.wheel_angle = min(self.wheel_angle, new_wheel_angle)  # don't overshoot
        elif new_wheel_angle < self.wheel_angle:
            self.wheel_angle -= self.wheel_actuation_speed * dt
            self.wheel_angle = max(self.wheel_angle, new_wheel_angle)  # don't overshoot
        self.wheel_angle = np.clip(
            self.wheel_angle, -self.max_wheel_angle, self.max_wheel_angle
        )
        new_speed = self.controller_throttle * self.max_speed
        if new_speed > self.speed:
            self.speed += self.accel * dt
        elif new_speed < self.speed:
            self.speed -= self.breaking_accel * dt
        self.speed = np.clip(self.speed, 0, self.max_speed)  # can't go backwards

        # physics loop
        self.angle += self.wheel_angle * self.speed * dt / self.turning_radius
        self.angle = (self.angle - 180) % 360 - 180  # keep between -180 -> 180
        self.velocity = self.speed * np.array(
            [np.sin(np.radians(self.angle)), -np.cos(np.radians(self.angle))]
        )
        self.center += self.velocity * dt

    def set_controls(self, throttle, steer):
        assert 0 <= throttle <= 1
        assert 0 <= steer <= 1

        self.controller_throttle = throttle
        self.controller_steer = steer

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
                self.velocity = 0
                return True

        return False

import numpy as np
from picar_sim.objects.base_object import Object


class Picar(Object):
    def __init__(
        self,
        controller,
        controller_interval=0,  # rate limit controller to simulate inference delay
        center=(0, 0),
        direction=0,
        max_speed=35,
    ):
        super().__init__(
            center=center,
            direction=direction,
            size=(16, 32),
            image_path="picar.png",
        )

        # controller variables
        self.controller = controller
        self.controller_interval = controller_interval
        self.dt_since_controller = 0  # to monitor controller update interval

        # dynamic variables
        self.speed = 0.0
        self.angle = 0.0  # NOT the same as self.direction which is car direction
        self.angular_velocity = 0.0

        # constants
        self.max_speed = max_speed
        self.angle_range = (50, 130)
        self.wheelbase = 14.4  # distance between front and back wheels for turn radius

    def update(self, dt, env):
        # check enough time has elapsed to update controls
        self.dt_since_controller += dt
        if self.dt_since_controller >= self.controller_interval:
            self.update_controls(dt, env)
            self.dt_since_controller = 0

        # update angular velocity and direction
        wheel_angle = self.angle - 90  # they use 90 as straight for some reason
        if abs(wheel_angle) > 0.01:  # avoid /0 error
            turn_radius = self.wheelbase / np.tan(np.radians(wheel_angle))
            angular_velocity = np.degrees(self.speed / turn_radius)
            self.direction = (self.direction + angular_velocity * dt) % 360  # 0->360

        # update velocity and position
        self.velocity = self.speed * np.array(
            [np.sin(np.radians(self.direction)), -np.cos(np.radians(self.direction))]
        )
        self.center += self.velocity * dt

    def update_controls(self, dt, env):
        angle, speed = self.controller.predict(picar=self, env=env)

        self.speed = np.clip(speed, 0, 35)  # ensure valid values
        self.angle = np.clip(angle, *self.angle_range)

        self.speed = self.speed / 35 * self.max_speed  # scale to max speed

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

from objects.base import SimulatorObject
import numpy as np
from controllers import KeyboardController
from grid_state import GridState


class Picar(SimulatorObject):
    def __init__(
        self,
        controller=KeyboardController(),
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

    def update(self, delta_time, objects):
        # get controls from controller
        throttle, steer = self.controller.get_controls()
        self.set_controls(throttle, steer)

        state = GridState()
        state.fetch_state(self, objects)
        state.print()

        # controls -> physics
        new_wheel_angle = (self.controller_steer * 2 - 1) * self.max_wheel_angle
        if new_wheel_angle > self.wheel_angle:
            self.wheel_angle += self.wheel_actuation_speed * delta_time
            self.wheel_angle = min(self.wheel_angle, new_wheel_angle)  # don't overshoot
        elif new_wheel_angle < self.wheel_angle:
            self.wheel_angle -= self.wheel_actuation_speed * delta_time
            self.wheel_angle = max(self.wheel_angle, new_wheel_angle)  # don't overshoot
        self.wheel_angle = np.clip(
            self.wheel_angle, -self.max_wheel_angle, self.max_wheel_angle
        )
        new_speed = self.controller_throttle * self.max_speed
        if new_speed > self.speed:
            self.speed += self.accel * delta_time
        elif new_speed < self.speed:
            self.speed -= self.breaking_accel * delta_time
        self.speed = np.clip(self.speed, 0, self.max_speed)  # can't go backwards

        # physics loop
        self.angle += self.wheel_angle * self.speed * delta_time / self.turning_radius
        self.angle = (self.angle - 180) % 360 - 180  # keep between -180 -> 180
        self.velocity = self.speed * np.array(
            [np.sin(np.radians(self.angle)), -np.cos(np.radians(self.angle))]
        )
        self.center += self.velocity * delta_time

    def set_controls(self, throttle, steer):
        assert 0 <= throttle <= 1
        assert 0 <= steer <= 1

        self.controller_throttle = throttle
        self.controller_steer = steer

        # def check_for_collisions(self, environment):
        #     if not self.can_collide:
        #         return

        #     for obj in environment:
        #         if not obj.can_collide or obj == self:
        #             continue

        #         distance = (
        #             np.linalg.norm(np.array(self.center) - np.array(obj.center))
        #             - np.mean(obj.size) / 2
        #             - np.mean(self.size) / 2
        #         )

        #         if distance < 0:
        #             return True

        #     return False

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

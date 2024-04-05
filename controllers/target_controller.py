import numpy as np


class TargetController:
    def __init__(self, picar):
        self.picar = picar

        self.targets = []

    def get_controls(self, *args):
        if len(self.targets) == 0:
            return 0, 0

        relative_target = self.targets[0] - self.picar.center

        # rotate target pos by -picar.angle
        angle = np.radians(-self.picar.angle)
        rotation_matrix = np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )
        relative_target = np.dot(rotation_matrix, relative_target)

        steer = relative_target[0] / 20 * 0.5 + 0.5
        steer = np.clip(steer, 0, 1)

        if np.linalg.norm(relative_target) < 5:
            self.targets.pop(0)

        return 1, steer

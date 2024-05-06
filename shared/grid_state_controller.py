import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from grid_state import GridState


class GridStateController:
    def __init__(self, *args, **kwargs):
        self.state = GridState(*args, **kwargs)

    def predict(self, image):  # for use on actual car
        self.state.observe_real(image)
        return self.predict_from_state(self.state)

    def predict_sim(self, picar, env):  # for use in simulation
        self.state.observe_sim(picar, env, range=60)
        return self.predict_from_state(self.state)

    def predict_from_state(self, state):  # override in controller subclass
        raise NotImplementedError

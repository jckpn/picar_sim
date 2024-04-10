# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

from controllers import PicarController, KeyboardController
from controllers.grid_state import GridState
import numpy as np


class GridStateController(PicarController):
    def __init__(self):
        self.state = GridState()
        self.kb_controller = KeyboardController()

        self.last_state = self.state.get_state()

    def get_controls(self, picar, env):
        self.state.update(picar, env)
        state = self.state.get_state()
        self.state.print()

        throttle, steer = self.kb_controller.get_controls()

        if not np.array_equal(state, self.last_state):
            with open("state_data.csv", "a") as f:
                f.write(f"{throttle},{steer}")
                for cell in self.state.state.flatten():
                    f.write(f",{str(cell)}")
                f.write("\n")

        self.last_state = state.copy()

        return throttle, steer

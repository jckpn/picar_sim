# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

from controllers import PicarController, KeyboardController
from controllers.grid_state import GridState


class GridCaptureController(PicarController):
    def __init__(self, base_controller=KeyboardController(), **grid_params):
        self.state = GridState(**grid_params)
        self.controller = base_controller
        self.ready = False

    def get_controls(self, picar, env):
        self.state.capture_state_from_env(picar, env, print=True)
        state = self.state.get_state()

        throttle, steer = self.controller.get_controls()

        if throttle > 0:
            self.ready = True  # only start capturing once user started moving

        if self.ready:
            with open("state_data.csv", "a") as f:
                f.write(f"{throttle},{steer}")
                for cell in self.state.state.flatten():
                    f.write(f",{str(cell)}")
                f.write("\n")

        self.last_state = state.copy()

        return throttle, steer

# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

from controllers import PicarController, KeyboardController
from shared.grid_state import GridState


class GridCaptureController(PicarController):
    def __init__(self, base_controller=KeyboardController()):
        self.state = GridState()
        self.controller = base_controller
        self.ready = False

    def get_controls(self, picar, env):
        self.state.capture_state_from_env(picar, env, print=True)
        track_state = self.state.get_layer("track")

        angle, speed = self.controller.get_controls()

        if angle > 0:
            self.ready = True  # only start capturing once user started moving

        if self.ready:
            with open("state_data.csv", "a") as f:
                # normalise
                angle = (angle - 50) / 80
                speed = speed / 35
                f.write(f"{angle},{speed}")
                for cell in track_state.flatten():
                    f.write(f",{str(cell)}")
                f.write("\n")

        return angle, speed

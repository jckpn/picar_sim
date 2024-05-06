# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

import os
import sys

sys.path.append('/Users/jckpn/dev/picar-sim/shared')

from controllers import KeyboardController
from grid_state_controller import GridStateController


class GridCaptureController(GridStateController):
    def __init__(self, base_controller=KeyboardController()):
        super().__init__()
        
        self.base_controller = base_controller
        self.ready = False

    def predict_from_state(self, state):
        angle, speed = self.base_controller.predict_from_state()
        
        track_state = state.get_layer("track")
        
        state.print()

        if speed > 0:
            self.ready = True  # only start capturing once user started moving

        if self.ready:
            with open("state_data.csv", "a") as f:
                # normalise
                norm_angle = (angle - 50) / 80
                norm_speed = speed / 35
                
                f.write(f"{norm_angle},{norm_speed}")
                for cell in track_state.flatten():
                    f.write(f",{str(cell)}")
                f.write("\n")

        return angle, speed

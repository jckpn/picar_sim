# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

from controllers import PicarController
from controllers.grid_state import GridState
from tensorflow import keras


class GridNeuralController(PicarController):
    def __init__(self, model_path):
        self.state = GridState()
        self.model = keras.models.load_model(model_path, safe_mode=False)

    def get_controls(self, picar, env):
        self.state.capture_state(picar, env)
        self.state.print()
        state = self.state.get_state()

        # check for intervention -- don't waste time predicting if collision coming
        # TODO

        # flatten and add batch dimension
        x = state.flatten().reshape(1, -1)
        pred = self.model(x)[0]
        throttle, steer = pred

        return throttle, steer

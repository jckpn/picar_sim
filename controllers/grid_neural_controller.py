# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

import numpy as np
from tensorflow import keras

from controllers import PicarController
from controllers.grid_state import GridState


class GridNeuralController(PicarController):
    def __init__(self, model_path, **grid_params):
        self.state = GridState(**grid_params)

        self.model = keras.models.load_model(model_path, safe_mode=False)
        self.model.trainable = False

    def get_controls(self, picar=None, env=None, state=None):
        if state is None:
            self.state.capture_state_from_env(picar, env, print=True)
            state = self.state.get_state()
            
        x = state.copy()
        x[x > 1] = 0  # ignore anything other than track
        x = np.expand_dims(x, axis=0)  # model expects batch dimension

        # call model to get action prediction
        pred = self.model(x)[0].numpy()

        # see if model predicts speed and steer, or just steer
        if len(pred) == 1:
            throttle, steer = 1.0, pred[0]  # full speed ahead!
        else:
            throttle, steer = pred

        throttle = np.clip(throttle, 0, 1)
        steer = np.clip(steer, 0, 1)

        return throttle, steer

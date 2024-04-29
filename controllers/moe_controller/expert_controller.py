# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

import numpy as np
from tensorflow import keras

from controllers import PicarController


class ExpertController(PicarController):
    def __init__(self, model_name):
        self.model_name = model_name
        model_path = f"controllers/moe_controller/models/{model_name}"
        self.model = keras.models.load_model(model_path, safe_mode=False, compile=False)
    
    def __str__(self):
        return self.model_name

    def get_controls(self, state, track_only=True):
        x = state == 1 if track_only else state.copy()

        # call model to get action prediction
        x = np.expand_dims(x, axis=0)  # model expects batch dimension
        y_hat = self.model(x)[0].numpy()

        # see if model predicts speed and steer, or just steer
        if len(y_hat) == 1:
            steer = y_hat[0]
            throttle = 1.0  # full speed ahead!
        else:
            throttle, steer = y_hat

        # clip to ensure valid values (e.g. relu might output slightly higher than 1)
        throttle = np.clip(throttle, 0, 1)
        steer = np.clip(steer, 0, 1)

        return throttle, steer
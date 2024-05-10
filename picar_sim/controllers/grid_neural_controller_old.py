# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

import numpy as np
from tensorflow import keras

from controllers import PicarController
from picar_sim.grid_state import GridState


class GridNeuralController(PicarController):
    def __init__(self, model_path, time_steps=None, **grid_params):
        self.state = GridState(**grid_params)
        self.time_steps = time_steps  # MAKE SURE THIS MATCHES MODEL

        self.model = keras.models.load_model(model_path, safe_mode=False)
        self.model.trainable = False

        self.state_sequence = []

    def get_controls(self, picar, env):
        self.state.capture_state_from_env(picar, env, print=True)
        state = self.state.get_state()

        # Check for intervention first -- don't want to waste time calling an inference
        # if a collision is imminent.
        # The intervation variable is a throttle multiplier so 0 = stop, 0.5 = slow
        # down, etc.

        # intervention = self.needs_intervention(state)
        intervention = 1  # to test raw model -- remove to enable
        # if intervention == 0:
        #     return 0, 0.5  # don't waste time predicting

        # x = np.eye(3)[state.astype(int)]  # one hot encode
        # x = x.reshape(
        #     self.state.grid_size, self.state.grid_size, 3
        # )  # transform back to grid
        # x = x[..., 1:]  # ignore first channel, nothing useful

        # if self.time_steps:
        #     self.state_sequence.append(x)
        #     if len(self.state_sequence) <= self.time_steps:
        #         return 0, 0.5
        #     self.state_sequence.pop(0)
        #     x = self.state_sequence.copy()[0]
        
        # x = state.flatten()
        
        x = state.copy()
        x[x > 1] = 0  # ignore anything other than track
        x = np.expand_dims(x, axis=0)  # model expects batch dimension

        # call model to get action prediction
        # pred = self.model(x)[0]
        # action = np.argmax(pred)

        # # convert to throttle/steer values
        # steer_bins = 17
        # actions = [[0, 0.5]] + [[1, a / (steer_bins - 1)] for a in range(steer_bins)]
        # throttle, steer = actions[action]
        
        throttle, steer = self.model(x)[0].numpy()
        throttle *= intervention  # apply intervention

        return throttle, steer

    # def needs_intervention(self, state):
    #     # intervention 1: no track detected
    #     if np.sum(state[-3:]) < 1:
    #         return 0

    #     # intervention 2: obstacle in immediate path
    #     for row in self.state.get_collision_cells(width=20, dist=20, offset_x=0):
    #         if self.state.encode_cell("Obstacle") in row:
    #             return 0

    #     # intervention 3: obstacle nearby, slow down
    #     for row in self.state.get_collision_cells(width=25, dist=50, offset_x=5):
    #         if self.state.encode_cell("Obstacle") in row:
    #             return 0.5

    #     return 1

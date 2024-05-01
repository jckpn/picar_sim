import numpy as np
from .cam_utils import overhead_warp, extract_track


class GridState:
    def __init__(self, size=30):
        self.size = size
        self.empty_state()

    def empty_state(self):
        empty = np.zeros((self.size, self.size))
        self.state = {
            "track": empty.copy(),
            "obstacle": empty.copy(),
            "red_traffic_light": empty.copy(),
            "turn_right_sign": empty.copy(),
            "turn_left_sign": empty.copy(),
        }

    def get_state_dict(self):
        return self.state.copy()

    def get_state_img(self):
        # return image where each layer is a diff channel
        num_layers = len(self.state)
        img = np.zeros((self.size, self.size, num_layers))
        for i, (layer_name, contents) in enumerate(self.state.items()):
            img[:, :, i] = contents
        return img

    def get_layer(self, layer_name):
        return self.state[layer_name].copy()

    def set_layer(self, layer_name, contents):
        self.state[layer_name] = contents.copy()

    def observe_sim(self, picar, env, range=60):
        self.empty_state()

        for object in env:
            if object == picar:
                continue  # don't need to capture self

            # get position of object from coords + relative direction
            position = object.center - picar.center
            direction = np.radians(-picar.direction)
            rotation = np.array([[np.cos(direction), -np.sin(direction)],
                                 [np.sin(direction), np.cos(direction)]])  # fmt: off
            position = np.dot(rotation, position)

            # offset to put picar at bottom-center
            offset_x = range / 2 + 2  # +2 camera x offset
            offset_y = range + 15  # +15 camera distance offset
            position += np.array([offset_x, offset_y])

            # quantise to state grid
            resolution = range / self.size
            position = np.array(position / resolution, dtype=int)

            # ignore if out of range
            if position.max() >= self.size or position.min() < 0:
                continue

            # add object to state
            try:  # don't want exception to stop loop
                object_name = object.__class__.__name__
                state_name = {
                    "TrackMaterial": "track",
                    "Obstacle": "obstacle",
                    "TrafficLight": "red_traffic_light",
                    "TurnRightSign": "turn_right_sign",
                    "TurnLeftSign": "turn_left_sign",
                }.get(object_name)

                self.state[state_name][position[1], position[0]] = 1

            except Exception as e:
                print(e)

    def observe_real(self, img):
        self.empty_state()

        img = overhead_warp(img)

        track_layer = extract_track(img)
        self.set_layer("track", track_layer)

    def print(self):
        for row in self.get_layer("track"):
            print("".join(["██" if cell > 0.5 else "░░" for cell in row]))

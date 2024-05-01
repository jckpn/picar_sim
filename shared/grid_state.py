import numpy as np


class GridState:
    def __init__(self, size=30):
        self.size = size

        empty = np.zeros((size, size))
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

    def observe_sim(self, picar, env, resolution=2):
        new_state = {}

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
            offset_x = self.size / 2 * resolution + 2  # +2 camera x offset
            offset_y = self.size * resolution + 15  # +15 camera distance offset
            position += np.array([offset_x, offset_y])

            # quantise to state grid
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
                if state_name not in new_state:
                    new_state[state_name] = np.zeros((self.size, self.size))
                new_state[state_name][position[1], position[0]] = 1
            except Exception as e:
                print(e)

        # only replace layer if it exists in new layer
        for layer_name, contents in new_state.items():
            if layer_name in self.state:
                self.state[layer_name] = contents
            else:
                self.state[layer_name] = np.zeros((self.size, self.size))

    def observe_real(self):
        pass

    def print(self):
        for row in self.get_layer("track"):
            print("".join(["██" if cell > 0.5 else "░░" for cell in row]))

import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cam_utils import extract_track, extract_obstacles


class GridState:
    def __init__(self, size=30):
        self.size = size
        self.empty_state()

    def empty_state(self):
        empty = np.zeros((self.size, self.size))
        self.state = {
            "track": empty.copy(),
            "obstacle": empty.copy(),
            "red_light": empty.copy(),
            "right_sign": empty.copy(),
            "left_sign": empty.copy(),
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

    def observe_real(self, img):
        self.empty_state()

        track_layer = extract_track(img)
        self.set_layer("track", track_layer)

        # obstacles = extract_obstacles(img)
        # for layer_name, position in obstacles:
        #     print(layer_name, position)
        #     x, y = position
        #     self.state[layer_name][y, x] = 1

    def print(self):
        img = self.get_state_img()
        for row in img:
            for px in row:
                px_str = "░░"

                if px[0] == 1:
                    px_str = "██"

                if px[1] == 1:
                    px_str = "XX"

                if px[2] == 1:
                    px_str = "RL"

                if px[3] == 1:
                    px_str = ">>"

                if px[4] == 1:
                    px_str = "<<"

                print(px_str, end="")
            print()

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
                    "TrafficLight": "red_light",
                    "TurnRightSign": "right_sign",
                    "TurnLeftSign": "left_sign",
                }.get(object_name)

                x, y = position
                self.state[state_name][y, x] = 1

            except Exception as e:
                print(e)


# test real-life observation
if __name__ == "__main__":
    import cv2

    img = cv2.imread("/Users/jckpn/dev/picar/data/training_data/training_data/26.png")
    state = GridState()
    state.observe_real(img)
    state.print()

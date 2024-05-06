import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from cam_utils import extract_track, extract_obstacles
from state_masks import sim_mask


class GridState:
    def __init__(self, size, obstacle_interval):
        self.size = size
        self.state = {}
        self.reset_state()

        self.run_counter = 0
        self.obstacle_interval = obstacle_interval

    def reset_layer(self, layer_name):
        self.state[layer_name] = np.zeros((self.size, self.size))

    def reset_state(self):
        for layer_name in ["track", "obstacle", "red_light", "right_sign", "left_sign"]:
            self.reset_layer(layer_name)

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
        self.run_counter += 1

        if self.run_counter >= self.obstacle_interval:
            self.reset_state()
            obstacles = extract_obstacles(img)
            for layer_name, position in obstacles:
                x, y = position
                self.state[layer_name][y, x] = 1
            self.run_counter = 0

        track_layer = extract_track(img)
        self.set_layer("track", track_layer)

    def observe_sim(self, picar, env, range=60):
        self.run_counter += 1

        update_obstacles = False
        if self.run_counter >= self.obstacle_interval:
            update_obstacles = True
            self.run_counter = 0
            self.reset_state()

        self.reset_layer("track")

        for object in env:
            if object == picar:
                continue  # don't need to capture self

            # get position of object from coords + relative direction
            position = object.center - picar.center
            direction = np.radians(-picar.direction)
            rotation = np.array(
                [
                    [np.cos(direction), -np.sin(direction)],
                    [np.sin(direction), np.cos(direction)],
                ]
            )
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
                    "RedLight": "red_light",
                    "RightSign": "right_sign",
                    "LeftSign": "left_sign",
                }.get(object_name)

                if state_name == "track" or update_obstacles:
                    x, y = position
                    self.state[state_name][y, x] = 1

            except Exception as e:
                print(e)

        self.state["track"] = self.state["track"] * sim_mask

    def print(self):
        img = self.get_state_img()
        for row in img:
            for px in row:
                px_str = "::"

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


# test real-life observation
if __name__ == "__main__":
    import cv2

    img = cv2.imread("/Users/jckpn/dev/picar/data/training_data/training_data/26.png")
    state = GridState()
    state.observe_real(img)
    state.print()

# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

import numpy as np


class GridState:
    def __init__(self, cell_size=4, max_distance=40):
        self.cell_size = cell_size  # cm
        self.max_distance = max_distance  # cm

        grid_size = max_distance * 2 // cell_size
        self.state = np.zeros((grid_size, grid_size), dtype=int)

        self.encoding = ["", "Picar", "Wood", "TrackMaterial"]
        self.display_encoding = [" ", "🚗", "🪵", "▫️"]

    def fetch_state(self, picar, env):
        # encode the current state of the picar and environment as a grid the picar is
        # always at the bottom-center of the grid (could experiment with picar at center
        # and calculating where objects behind it are)

        # IMPORTANT: objects inside track must be inside track in the grid state too!
        # might need way to encode car speed and wheel angle too? not sure how important
        # they'll be

        for obj in env:
            obj_name = obj.__class__.__name__
            obj_pos = obj.center - picar.center

            # rotate targets pos by picar angle
            angle = np.radians(-picar.angle)
            rotation_matrix = np.array(
                [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
            )
            obj_pos = np.dot(rotation_matrix, obj_pos)

            # ignore if out of range
            if obj_pos.max() > self.max_distance or obj_pos.min() < -self.max_distance:
                continue

            # quantise position to grid
            obj_pos = np.array(obj_pos // self.cell_size, dtype=int)

            # offset so picar is at center
            obj_pos += self.state.shape[0] // 2

            try:
                if self.state[obj_pos[1], obj_pos[0]] != 0:
                    # don't overwrite existing objects
                    continue
                self.state[obj_pos[1], obj_pos[0]] = self.encoding.index(obj_name)
            except Exception:  # don't want exceptions to stop the loop
                pass

    def print(self):
        print("\n" * 10)
        
        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                print(self.display_encoding[cell], end=" ")
            print()

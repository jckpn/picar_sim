# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

# it's important that the state is as concise as possible

# things which MUST be included in the state (i.e. things that could affect the desired
# behaviour):

#   1.  the car's position within the tracks (could be single value?)

#   2.  the presence of any obstacles, if in the way of desired path (most obstacles
#       outside of path can be ignored)

#   3.  the presence of RED traffic lights outside of path (ignore green)

#   4.  the presence of a junction, and which way the sign indicates to go

# these can be used to form a desired path or perhaps a single target point, which a
# simple model can be used to follow via speed/steer values

# single target point for simple stuff like following a road, multiple target points
# for complex stuff like junctions?

# ideally compare this with standard approach (cnn -> controls) and transformer approach


import numpy as np


class GridState:  # TODO: figure out what grid size corresponds to the view we get
    def __init__(self, range=100, cell_size=3):
        self.cell_size = cell_size  # cm
        self.range = range  # cm
        self.grid_size = range // cell_size  # cells

        self.encoding = [None, "TrackMaterial", "Wood", "Picar"]  # name -> int
        self.display_encoding = [" ", "*", " ", " "]  # int -> symbol

        self.reset()

    def reset(self):
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=int)

    def get_state(self):
        return self.state.copy()

    def update(self, picar, env):
        # encode the current state of the picar and environment as a grid the picar is
        # always at the bottom-center of the grid (could experiment with picar at center
        # and calculating where objects behind it are)

        # IMPORTANT: objects inside track must be inside track in the grid state too!
        # might need way to encode car speed and wheel angle too? not sure how important
        # they'll be

        self.reset()

        for obj in env:
            obj_name = obj.__class__.__name__
            obj_pos = obj.center - picar.center

            # rotate targets pos by picar angle
            angle = np.radians(-picar.angle)
            rotation_matrix = np.array(
                [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
            )
            obj_pos = np.dot(rotation_matrix, obj_pos)

            # quantise position to grid
            obj_pos = np.array(obj_pos // self.cell_size, dtype=int)

            # offset so picar is at bottom center
            obj_pos += np.array([self.grid_size // 2, self.grid_size])

            # ignore if out of range
            if obj_pos.max() > self.grid_size or obj_pos.min() < 0:
                continue

            try:
                self.state[obj_pos[1], obj_pos[0]] = self.encoding.index(obj_name)
            except Exception:  # don't want exceptions to stop the loop
                pass

    def print(self):
        print("\n" * 10)

        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                print(self.display_encoding[cell], end=" ")
            print()

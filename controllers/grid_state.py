# get the picar's state as a grid

# things which MUST be included in the state (i.e. things that could affect the desired
# behaviour):
#   1.  the tracks, or car's position within the tracks
#   2.  the presence of any obstacles, if in the way of desired path (most obstacles
#       outside of path can be ignored)
#   3.  the presence of RED traffic lights outside of path (ignore green)
#   4.  the presence of a junction, and which way the sign indicates to go
#   5. more?

# ideally compare this with standard approach (cnn -> controls)

# TODO: picar should be trained to not move unless track is detected
# (intervention model can handle this)
# TODO: unknown obstacles should be detected too

import numpy as np


class GridState:  # TODO: figure out what grid size corresponds to the view we get
    def __init__(self, range=100, cell_size=3):
        self.cell_size = cell_size  # cm
        self.range = range  # cm
        self.grid_size = range // cell_size  # cells

        self.encoding = {  # capture state as integers
            "Empty": 0,
            "GreenTrafficLight": 0,  # ignore as no effect on desired behaviour
            "TrackMaterial": 1,
            "Obstacle": 2,  # pedestrians etc
            "RedTrafficLight": 3,
            "TurnRightSign": 4,
            "TurnLeftSign": 5,
        }

        self.display_encoding = [  # -> symbol
            " ",
            ".",
            "O",
            "R",
            ">",
            "<",
        ]

        # idea: each object has own layer in grid state, then can use small CNN

        self.reset()

    def reset(self):
        self.state = np.zeros((self.grid_size, self.grid_size), dtype=int)

    def get_state(self):
        return self.state.copy()

    def capture_state(self, picar, env):
        # encode the current state of the picar and environment as a grid the picar is
        # always at the bottom-center of the grid (could experiment with picar at center
        # and calculating where objects behind it are)

        # IMPORTANT: objects inside track must be inside track in the grid state too!
        # might need way to encode car speed and wheel angle too? not sure how important
        # they'll be

        self.reset()

        for obj in env:
            if obj == picar:  # don't waste data capturing self
                continue

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
                self.state[obj_pos[1], obj_pos[0]] = self.encoding[obj_name]
            except Exception:  # don't want exceptions to stop the loop
                pass

    def estimate_state(self, picar, dt):
        # estimate the picar's position based on its speed and angle in case object
        # detection inferences are too slow etc

        # convert current state to list of objects with positions
        # ...

        # update positions based on speed and angle
        # ...
        pass

    def print(self):
        print("\n" * 10)

        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                print(self.display_encoding[cell], end=" ")
            print()

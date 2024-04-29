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
    def __init__(self, range=None, cell_size=None, grid_size=None, camera_offset=12.0):
        assert cell_size and (range or grid_size)
        assert not range or range % cell_size == 0, "range must be divisible by cell_size"

        self.cell_size = cell_size  # cm
        self.range = range if range else grid_size * cell_size
        self.grid_size = grid_size if grid_size else int(range / cell_size)

        # apply offset since picar doesn't see from its actual center
        self.camera_offset = camera_offset

        # capture state as integers, probs most efficient way to store for now
        self.cell_obj_to_int = {
            "Empty": 0,
            "GreenTrafficLight": 0,  # ignore as no effect on desired behaviour
            "TrackMaterial": 1,
            "Obstacle": 2,  # pedestrians etc
            "RedTrafficLight": 3,
            "TurnRightSign": 4,
            "TurnLeftSign": 5,
        }

        self.cell_int_to_str = [  # convert state to symbols, e.g. for pattern matching
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

    def get_state_as_str(self):
        state_str = ""
        for y, row in enumerate(self.state):
            for x, cell in enumerate(row):
                state_str += self.cell_int_to_str[cell]
            state_str += "\n"
        return state_str

    def capture_state_from_env(self, picar, env, print=True):
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
            obj_pos += np.array([
                    self.grid_size / 2,
                    self.grid_size + self.camera_offset / self.cell_size,
                ], dtype=int)  # fmt: off

            # ignore if out of range
            if obj_pos.max() > self.grid_size or obj_pos.min() < 0:
                continue

            if obj_name == "TrafficLight":
                if obj.state == "red":
                    obj_name = "RedTrafficLight"
                elif obj.state == "green":
                    obj_name = "GreenTrafficLight"

            try:
                self.state[obj_pos[1], obj_pos[0]] = self.cell_obj_to_int[obj_name]
            except Exception:  # don't want exceptions to stop the loop
                pass

        self.state = self.simulate_view_obstructions(self.state)

        if print:
            self.print()

    def simulate_view_obstructions(self, state):
        for y, row in enumerate(state):
            for x, cell in enumerate(row):
                if cell == self.cell_obj_to_int["Obstacle"]:
                    # make all cells behind obstacle empty
                    state[: y - 1, x] = self.cell_obj_to_int["Empty"]
        return state

    def get_collision_cells(self, width, dist, offset_x=0):
        # work out the cells in collision path of picar
        # maybe: this should change size/shape based on speed and angle?
        grid_width = width // self.cell_size
        grid_height = dist // self.cell_size
        x = self.grid_size // 2 - grid_width // 2
        offset_x = offset_x // self.cell_size
        return self.state[-grid_height:, offset_x + x : offset_x - x]

    def estimate_state(self, picar, dt):
        # estimate the picar's position based on its speed and angle in case object
        # detection inferences are too slow etc

        # convert current state to list of objects with positions
        # ...

        # update positions based on speed and angle
        # ...
        pass

    def to_cm(self, grid_size):
        return grid_size * self.cell_size

    def print(self):
        state_str = self.get_state_as_str()

        for row in state_str.split("\n"):
            for cell in state_str:
                print(cell, end=" ")
            print()

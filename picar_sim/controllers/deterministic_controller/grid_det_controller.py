# grid state with deterministic policy

# get the picar's state as a grid
# putting this in its different file because it feels important lol

# TODO: note picar should be trained to not move unless track is detected

import numpy as np

from controllers import PicarController
from picar_sim.grid_state import GridState


class GridDetController(PicarController):
    def __init__(self, **grid_params):
        self.state = GridState(**grid_params)
        self.throttle = 0
        self.steer = 0
        
        # idea:
        # gating model could choose
        # 1. stop/wait
        # 2. follow track
        # 3. turn right at junction
        # 4. turn left at junction
        # 5. go straight at junction
        # where these are each small, separate models to be trained

        self.rules = [  # these are applied in order
            self.stop_if_no_track,
            self.stop_if_obstacle_in_front,
            self.slowdown_if_obstacle_in_path,
            self.steer_to_follow_track,
            self.clip_between_0_1,
        ]

    def get_controls(self, picar, env):
        self.state.capture_state_from_env(picar, env, print=True)
        state = self.state.get_state_as_str()
        for rule in self.rules:
            rule(state)
            print(f"Rule {rule.__name__}: throttle={self.throttle}, steer={self.steer}")
        return self.throttle, self.steer

    # define rules (remember to add to array in init fn)
    def stop_if_no_track(self, state):
        matches = self.find_in_state(".")
        self.throttle += 0.1 if len(matches) > 0 else -0.1
        self.throttle = np.clip(self.throttle, 0, 1)

    def stop_if_obstacle_in_front(self, state):
        # obstacle in immediate path, failsafe
        matches = self.find_in_state("O")
        if len(matches) == 0:
            return

        for x, y in matches:
            print(x, y)
            if x > -10 and x < 20 and y < 10:  # offset x towards track
                self.throttle = 0
                return

    def slowdown_if_obstacle_in_path(self, state):
        matches = self.find_in_state(obstacle_patterns)

        if len(matches) == 0:
            return

        # only want the closest obstacle
        closest_y = min([y for x, y in matches])
        if closest_y < 40:
            self.throttle *= 0.6
        if closest_y < 20:
            self.throttle *= 0.3
        self.throttle = np.clip(self.throttle, 0, 1)

    def steer_to_follow_track(self, state):
        # basic implementation -- follow left-most track cell
        target_left = 7  # this is where we WANT the call to be

        # TODO: redo with find_in_state
        track_row = state.split("\n")[-3]
        if "." not in track_row:
            return  # handled by can_see_track
        leftmost_track_cell = track_row.index(".")
        if leftmost_track_cell == -1:
            self.steer = 0.0
            return
        direction = 1 if leftmost_track_cell > target_left else -1
        magnitude = abs(leftmost_track_cell - target_left) * 0.3  # magic number
        self.steer = direction * magnitude * 0.5 + 0.5

    def clip_between_0_1(self, state):
        self.throttle = np.clip(self.throttle, 0, 1)
        self.steer = np.clip(self.steer, 0, 1)

    def find_in_state(self, patterns):
        # e.g. str might be " . \n . \n . " want to see if this is in the state, which
        # has longer lines. return position of str in state, kind of like a conv op

        state = self.state.get_state_as_str()
        state = state.split("\n")
        state_h = len(state)
        state_w = len(state[0])

        if isinstance(patterns, str):
            patterns = [patterns]

        matches = []

        for pat in patterns:
            pat = pat.split("\n")
            pat_h = len(pat)
            pat_w = len(pat[0])

            # slide pattern along state to find pattern
            for y in range(state_h - pat_h):
                rows = state[y : y + pat_h]
                for x in range(state_w - pat_w):
                    columns = [row[x : x + pat_w] for row in rows]
                    if columns == pat:
                        match = (
                            self.state.to_cm(x - state_w // 2),
                            self.state.to_cm(state_w - y),
                        )  # give relative distance from picar (bottom center of state)
                        matches.append(match)

        return matches


obstacle_patterns = [  # todo: generate a file with every 'halt' pattern and use that?
    ".\nO\n.",
    ".O    .",
    ". O   .",
    ".  O  .",
    ".   O .",
    ".    O.",
    ".O     .",
    ". O    .",
    ".  O   .",
    ".   O  .",
    ".    O .",
    ".     O.",
    # middle line not detected:
    ".O         ."
    ". O        ."
    ".  O       ."
    ".   O      ."
    ".    O     ."
    ".     O    .",
    ".O          ."
    ". O         ."
    ".  O        ."
    ".   O       ."
    ".    O      ."
    ".     O     .",
]

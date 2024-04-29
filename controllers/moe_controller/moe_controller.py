import numpy as np

from controllers import PicarController
from controllers.grid_state import GridState
from .expert_controller import ExpertController


class MoeController(PicarController):
    def __init__(self, initial_expert="follow", smoothing=0.8, **grid_params):
        self.state = GridState(**grid_params)

        # initialise models
        self.experts = {
            "follow": ExpertController("combined_junction_straight.keras"),
            # "left_turns": ExpertController("left_turns.keras"),
            # "right_turns": ExpertController("right_turns.keras"),
            # "wait_at_junction": ExpertController("follow.keras"),  # TODO
        }
        self.current_expert = self.experts[initial_expert]
        self.smoothing = smoothing
        self.last_controls = [0.0, 0.5]

    def get_controls(self, picar, env):  # talk about order/priority of operations here
        self.state.capture_state_from_env(picar, env, print=True)
        state = self.state.get_state()
        self.update_gate(state)

        # check for intervention
        # if obstacle in direct path, stop...

        expert_controls = self.current_expert.get_controls(state=state)
        s = self.smoothing
        expert_controls = [
            (1 - s) * expert_controls[i] + s * self.last_controls[i] for i in range(2)
        ]
        self.last_controls = expert_controls
        print(f"{str(self.current_expert)}: {expert_controls}")
        return expert_controls

    def update_gate(self, state):
        if np.random.rand() < 1:
            return

        best_expert = "right_turns" if np.random.rand() < 0.5 else "left_turns"

        self.current_expert = self.experts[best_expert]

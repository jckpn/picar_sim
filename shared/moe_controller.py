import numpy as np
from .grid_state_controller import GridStateController
from .expert_controller import ExpertController


class MoeController(GridStateController):
    def __init__(self, initial_expert="follow", smoothing=0.0):
        super().__init__()

        # initialise models
        self.experts = {
            "follow": ExpertController(
                "follow_30_binary", track_only=True, steer_only=True
            ),
            # "left_turns": ExpertController("left_turns.keras"),
            # "right_turns": ExpertController("right_turns.keras"),
            # "wait_at_junction": ExpertController("follow.keras"),  # TODO
        }
        self.current_expert = self.experts[initial_expert]
        self.smoothing = smoothing
        self.last_angle = 0
        self.last_speed = 0

    def predict_from_state(self, state):  # talk about order/priority of operations here
        intervention = self.check_interventions(state)
        if intervention is not None:
            print(f"!! INTERVENTION: {intervention.message} !!")
            return intervention  # don't bother with smoothing if urgent intervention

        # if no urgent intervention, get controls as normal
        self.update_gate(state)

        angle, speed = self.current_expert.predict_from_state(state)

        # state.print()
        # print(f"{str(self.current_expert)}: angle={angle}, speed={speed}")

        # apply smoothing
        if self.smoothing > 0:
            angle = (1 - self.smoothing) * angle + self.smoothing * self.last_angle
            speed = (1 - self.smoothing) * speed + self.smoothing * self.last_speed
            self.last_angle, self.last_speed = angle, speed

        return angle, speed

    def update_gate(self, state):
        return

        best_expert = "right_turns" if np.random.rand() < 0.5 else "left_turns"

        self.current_expert = self.experts[best_expert]

    def check_interventions(self, state):
        # check if any obstacles in immediate

        obstacle_layer = state.get_layer("obstacle")

        obstacle_layer = obstacle_layer[0:15, :]  # only check closest 30cm
        if np.sum(obstacle_layer) > 0:
            return {
                "message": "obstacle in path!",
                "angle": 90,
                "speed": 0,
            }

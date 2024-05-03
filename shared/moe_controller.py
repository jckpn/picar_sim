import numpy as np
from .grid_state_controller import GridStateController
from .expert_controller import ExpertController


class MoeController(GridStateController):
    def __init__(self, default_expert="follow", smoothing=0.0):
        super().__init__()

        # initialise models
        self.experts = {
            "follow": ExpertController("follow_30", steer_only=True),
            "left_turns": ExpertController("follow_30", steer_only=True),
            "right_turns": ExpertController("follow_30", steer_only=True),
        }
        self.default_expert = default_expert
        self.current_expert = self.experts[default_expert]

        # init vars for smoothing
        self.smoothing = smoothing
        self.last_angle = 90
        self.last_speed = 0

    def predict_from_state(self, state):  # talk about order/priority of operations here
        intervention = self.check_interventions(state)
        if intervention is not None:
            state.print()
            print(f"!! INTERVENTION: {intervention['message']} !!")

            # don't apply smoothing, but store it for smoother speed-up
            self.last_angle = intervention["angle"]
            self.last_speed = intervention["speed"]
            return intervention["angle"], intervention["speed"]

        # if no urgent intervention, get controls as normal
        self.update_gate(state)
        angle, speed = self.current_expert.predict_from_state(state)

        # state.print()

        # state.print()
        # print(f"{str(self.current_expert)}: angle={angle}, speed={speed}")

        # apply smoothing
        if self.smoothing > 0:
            angle = (1 - self.smoothing) * angle + self.smoothing * self.last_angle
            speed = (1 - self.smoothing) * speed + self.smoothing * self.last_speed
            self.last_angle, self.last_speed = angle, speed

        return angle, speed

    def update_gate(self, state):
        new_expert = self.default_expert
        
        left_sign_layer = state.get_layer("left_sign")
        right_sign_layer = state.get_layer("right_sign")
        
        if np.sum(left_sign_layer) > np.sum(right_sign_layer):
            new_expert = "left_turns"
        elif np.sum(right_sign_layer) > np.sum(left_sign_layer):
            new_expert = "right_turns"

        self.current_expert = self.experts[new_expert]

    def check_interventions(self, state):
        # check if any obstacles in immediate collision path
        # path_mask = np.zeros((state.size, state.size))
        obstacle_layer = state.get_layer("obstacle")
        obstacle_layer = obstacle_layer[15:, 10:20]  # bottom-center 6th of grid
        if np.sum(obstacle_layer) > 0:
            return {
                "message": "OBSTACLE IN PATH",
                "angle": 90,
                "speed": 0,
            }

        # check if obstacles in steering path
        # ...

        # check if any red lights
        red_light_layer = state.get_layer("red_light")
        red_light_layer = red_light_layer[20:, :]  # check sides of grid
        if np.sum(red_light_layer) > 0:
            return {
                "message": "RED LIGHT",
                "angle": 90,
                "speed": 0,
            }

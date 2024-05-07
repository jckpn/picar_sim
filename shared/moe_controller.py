import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from grid_state_controller import GridStateController
from expert_controller import ExpertController
import state_masks


class MoeController(GridStateController):
    def __init__(
        self,
        default_expert="follow",
        smoothing=0.0,
        state_size=30,
        obstacle_interval=5,  # 
        gate_reset_delay=1,  # 
        print_state=False,
    ):
        super().__init__(state_size, obstacle_interval)

        # initialise models
        self.experts = {
            "follow": ExpertController("follow_30", steer_only=True),
            "left_turns": ExpertController("left_30", steer_only=True),
            "right_turns": ExpertController("right_30", steer_only=True),
        }
        self.current_expert = self.experts[default_expert]
        self.default_expert = self.current_expert

        # init vars for smoothing
        self.smoothing = smoothing
        self.last_angle = 90
        self.last_speed = 0

        self.print_state = print_state

        self.gate_reset_delay = gate_reset_delay
        self.gate_counter = 0

    def predict_from_state(self, state):  # talk about order/priority of operations here
        intervention = self.check_interventions(state, self.last_angle, self.last_speed)
        if intervention is not None:
            state.print()
            print(f"!! INTERVENTION: {intervention['message']} !!")

            # don't apply smoothing, but store it for smoother speed-up
            self.last_angle = intervention["angle"]
            self.last_speed = intervention["speed"]
            return intervention["angle"], intervention["speed"]

        # if no urgent intervention, get controls as normal
        self.gate_counter += 1
        if (
            self.current_expert == self.default_expert
            or self.gate_counter >= self.gate_reset_delay
        ):
            self.update_gate(state)
            self.gate_counter = 0

        angle, speed = self.current_expert.predict_from_state(state)

        if self.print_state:
            state.print()
            print(f"{str(self.current_expert)}: angle={angle}, speed={speed}")

        # apply smoothing
        if self.smoothing > 0:
            angle = (1 - self.smoothing) * angle + self.smoothing * self.last_angle
            speed = (1 - self.smoothing) * speed + self.smoothing * self.last_speed
            self.last_angle, self.last_speed = angle, speed

        return angle, speed

    def check_interventions(self, state, angle, speed):
        # check if any obstacles in collision path
        # calculate path of car from angle

        path_mask = self.get_path_mask(angle, speed)

        obstacle_layer = state.get_layer("obstacle")
        obstacle_layer = obstacle_layer * path_mask  # bitwise and
        if np.sum(obstacle_layer) > 0:
            return {
                "message": "OBSTACLE IN PATH",
                "angle": 90,
                "speed": 0,
            }

        # check if any red lights within 30cm
        red_light_layer = state.get_layer("red_light")
        red_light_layer = red_light_layer[15:, :]
        if np.sum(red_light_layer) > 0:
            return {
                "message": "RED LIGHT",
                "angle": 90,
                "speed": 0,
            }

    def update_gate(self, state):
        left_sign_layer = state.get_layer("left_sign")
        right_sign_layer = state.get_layer("right_sign")

        if np.sum(left_sign_layer) > 1:
            self.current_expert = self.experts["left_turns"]
        elif np.sum(right_sign_layer) > 1:
            self.current_expert = self.experts["right_turns"]
        else:
            self.current_expert = self.default_expert

    def get_path_mask(self, angle, speed):
        if angle < 80:
            return state_masks.left_turn
        elif angle > 100:
            return state_masks.right_turn
        else:
            return state_masks.straight_path

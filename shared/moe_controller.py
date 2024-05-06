import numpy as np
from .grid_state_controller import GridStateController
from .expert_controller import ExpertController


class MoeController(GridStateController):
    def __init__(self, default_expert="follow", smoothing=0.0, obstacle_interval=1):
        super().__init__(obstacle_interval)

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
        self.update_gate(state)
        angle, speed = self.current_expert.predict_from_state(state)

        state.print()

        # state.print()
        print(f"{str(self.current_expert)}: angle={angle}, speed={speed}")

        # apply smoothing
        if self.smoothing > 0:
            angle = (1 - self.smoothing) * angle + self.smoothing * self.last_angle
            speed = (1 - self.smoothing) * speed + self.smoothing * self.last_speed
            self.last_angle, self.last_speed = angle, speed

        return angle, speed

    def update_gate(self, state):
        # if self.current_expert != self.default_expert:
        #     print(str(self.current_expert), str(self.default_expert))
        #     return  # already changed expert

        left_sign_layer = state.get_layer("left_sign")
        right_sign_layer = state.get_layer("right_sign")

        if np.sum(left_sign_layer) > 1:
            self.current_expert = self.experts["left_turns"]
        elif np.sum(right_sign_layer) > 1:
            self.current_expert = self.experts["right_turns"]

    def check_interventions(self, state, angle, speed):
        # check if any obstacles in collision path
        # calculate path of car from angle

        path_mask = self.get_path_mask(state, angle, speed)

        obstacle_layer = state.get_layer("obstacle")
        obstacle_layer = obstacle_layer * path_mask  # bitwise and
        if np.sum(obstacle_layer) > 0:
            return {
                "message": "OBSTACLE IN PATH",
                "angle": 90,
                "speed": 0,
            }

        # check if any red lights around
        red_light_layer = state.get_layer("red_light")
        red_light_layer = red_light_layer[15:, :]
        if np.sum(red_light_layer) > 0:
            return {
                "message": "RED LIGHT",
                "angle": 90,
                "speed": 0,
            }

    def get_path_mask(self, state, angle, speed):
        path_mask = np.zeros((state.size, state.size))
        lookahead_time = 1
        path_dist = int(speed * lookahead_time)
        
          # immediate collisions
        path_mask[-path_dist // 4 :, 10:20] = 1
         # imminent collisions
         
        if angle > 100:
            path_mask[-path_dist // 2 :, 12:30] = 1
        elif angle < 80:
            path_mask[-path_dist // 2 :, 0:18] = 1
        else:
            path_mask[-path_dist // 2 :, 10:20] = 1

        return path_mask

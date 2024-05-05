from picar_sim import PicarSim
import objects
import numpy as np

# TODO: randomise obstacles. add random obstacles to all scenes out of way of track


# 1. Keeping in lane driving along the straight section of the T-junction track, as
# shown in Fig. 1.
class Scene1(PicarSim):
    def __init__(self, controller, controller_interval=0.1, **kwargs):
        super().__init__(
            picar=objects.Picar(
                controller, controller_interval, center=(-150, -10), direction=90
            ),
            track=objects.tracks.Junction(),
            **kwargs,
        )


# 2. As (1), but driving as normal if pedestrians or other objects are on the side of
# (but not in) the road, as shown in Fig. 2.
class Scene2(Scene1):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_random_obstacles(-150, -30, 100, -25)


# 3. As (1), but stopping if a pedestrian is in the road, as shown in Fig. 3.
class Scene3(Scene1):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_random_obstacles(-150, -25, 100, 25)


# 4. Driving around the oval track in both directions, as shown in Fig. 4.
class Scene4(PicarSim):
    def __init__(self, controller, controller_interval=0.1, **kwargs):
        start_pos = (
            {
                "center": (-150, 0),
                "direction": 0,
            }
            if np.random.rand() < 0.5
            else {
                "center": (-120, 0),
                "direction": 180,
            }
        )
        super().__init__(
            picar=objects.Picar(controller, controller_interval, **start_pos),
            track=objects.tracks.Oval(),
            **kwargs,
        )


# 5. As (4), but driving as normal if pedestrians or other objects are on the side of
# (but not in) the road, as shown in Fig. 5.
class Scene5(Scene4):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.obstacle_regions = [
            (-68, -21, 136, 42),  # inside oval
            (-145, -80, 37, 160),  # left side (outside)
            (-150, -100, 300, 40),  # upper side
            (112, -80, 37, 160),  # right side
            (-150, 60, 300, 40),  # lower side
        ]


# 6. As (4), but stopping if a pedestrian is in the road, as shown in Fig. 6.
class Scene6(Scene4):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.obstacle_regions = [(-100, -50, 200, 100)]


# 7. Driving around the figure-of-eight, continuing straight at the intersection, as
# shown in Fig. 7.
class Scene7(PicarSim):
    def __init__(self, controller, controller_interval=0.1, **kwargs):
        start_pos = (
            {
                "center": (-150, 0),
                "direction": 0,
            }
            if np.random.rand() < 0.5
            else {
                "center": (-130, 0),
                "direction": 180,
            }
        )
        super().__init__(
            picar=objects.Picar(controller, controller_interval, **start_pos),
            track=objects.tracks.Figure8(),
            **kwargs,
        )


# 8. Stopping due to an object in the center of the intersection, as shown in Fig. 8.
class Scene8(Scene7):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_random_obstacles(-30, -30, 30, 30)


# 9. Stopping due to a red traffic light at the intersection, then continuing when it
# changes to green, as shown in Fig. 9.

class Scene9(Scene7):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_objects([objects.RedLight(center=(0, -40))])

# 10. Performing a left turn at the T-junction, in response to a traffic sign, as shown
# in Fig. 10. We will place 2 left turn signs at positions indicated in the figure.


class Scene10(Scene1):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_objects(
            [
                objects.LeftSign(center=(145, -10)),
                objects.LeftSign(center=(145, 10)),
            ]
        )


# 11. Performing a right turn at the T-junction, in response to a traffic sign, as shown
# in Fig. 11. We will place 2 right turn signs at positions indicated in the figure.
# Note this ‘unprotected’ right (left in the USA) has been a major difficulty in
# the Tesla autonomous beta testing program.
class Scene11(Scene1):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_objects(
            [
                objects.RightSign(center=(145, -10)),
                objects.RightSign(center=(145, 10)),
            ]
        )

# 12. Driving round the oval track, as (4), but at a speed of 50. Can your car respond
# fast enough at this speed?

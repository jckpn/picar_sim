from picar_sim import PicarSim
import objects
import numpy as np

# TODO: randomise obstacles. add random obstacles to all scenes out of way of track


# 1. Keeping in lane driving along the straight section of the T-junction track, as
# shown in Fig. 1.
class Scene1(PicarSim):
    def __init__(self, **kwargs):
        super().__init__(
            picar=objects.Picar(center=(-100, -10), angle=90),
            track=objects.tracks.Junction(),
            **kwargs,
        )


# 2. As (1), but driving as normal if pedestrians or other objects are on the side of
# (but not in) the road, as shown in Fig. 2.
class Scene2(Scene1):
    def __init__(self, **kwargs):
        super().__init__(
            obstacles=[  # TODO: randomise these
                objects.obstacles.Wood(center=(-50, -50)),
            ],
            **kwargs,
        )


# 3. As (1), but stopping if a pedestrian is in the road, as shown in Fig. 3.
class Scene3(Scene1):
    def __init__(self, **kwargs):
        super().__init__(
            obstacles=[
                objects.obstacles.Wood(center=(-50, -10)),
            ],
            **kwargs,
        )


# 4. Driving around the oval track in both directions, as shown in Fig. 4.
class Scene4(PicarSim):
    def __init__(self, **kwargs):
        super().__init__(
            picar=objects.Picar(center=(0, -45), angle=-90),
            track=objects.tracks.Oval(),
            **kwargs,
        )

        if np.random.rand() > 0.5:
            self.picar.center = (0, -65)
            self.picar.angle = 90


# 5. As (4), but driving as normal if pedestrians or other objects are on the side of
# (but not in) the road, as shown in Fig. 5.
class Scene5(Scene4):
    def __init__(self, **kwargs):
        super().__init__(
            obstacles=[
                objects.obstacles.Wood(center=(0, -10)),
            ],
            **kwargs,
        )


# 6. As (4), but stopping if a pedestrian is in the road, as shown in Fig. 6.
class Scene6(Scene4):
    def __init__(self, **kwargs):
        super().__init__(
            obstacles=[
                objects.obstacles.Wood(center=(0, -45)),
            ],
            **kwargs,
        )


# 7. Driving around the figure-of-eight, continuing straight at the intersection, as
# shown in Fig. 7.
class Scene7(PicarSim):
    def __init__(self, **kwargs):
        super().__init__(
            picar=objects.Picar(center=(0, -45), angle=-90),
            track=objects.tracks.Figure8(),
            **kwargs,
        )

        if np.random.rand() > 0.5:
            self.picar.center = (0, -65)
            self.picar.angle = 90


# 8. Stopping due to an object in the center of the intersection, as shown in Fig. 8.
class Scene8(Scene7):
    def __init__(self, **kwargs):
        super().__init__(
            obstacles=[
                objects.obstacles.Wood(center=(0, 0)),
            ],
            **kwargs,
        )


# 9. Stopping due to a red traffic light at the intersection, then continuing when it
# changes to green, as shown in Fig. 9.
class Scene9(Scene7):
    def __init__(self, **kwargs):
        super().__init__(
            obstacles=[
                # objects.obstacles.TrafficLight(center=(0, 0), color="red"),
            ],
            **kwargs,
        )


# 10. Performing a left turn at the T-junction, in response to a traffic sign, as shown
# in Fig. 10. We will place 2 left turn signs at positions indicated in the figure.
class Scene10(Scene1):
    def __init__(self, **kwargs):
        super().__init__(
            obstacles=[
                # objects.obstacles.TrafficSign(center=(0, 0), direction="left"),
                # objects.obstacles.TrafficSign(center=(0, 0), direction="left"),
            ],
            **kwargs,
        )


# 11. Performing a right turn at the T-junction, in response to a traffic sign, as shown
# in Fig. 11. We will place 2 right turn signs at positions indicated in the figure.
# Note this ‘unprotected’ right (left in the USA) has been a major difficulty in
# the Tesla autonomous beta testing program.
class Scene11(Scene1):
    def __init__(self, **kwargs):
        super().__init__(
            obstacles=[
                # objects.obstacles.TrafficSign(center=(0, 0), direction="right"),
                # objects.obstacles.TrafficSign(center=(0, 0), direction="right"),
            ],
            **kwargs,
        )


# 12. Driving round the oval track, as (4), but at a speed of 50. Can your car respond
# fast enough at this speed?
class Scene12(Scene4):
    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )

        self.picar.max_speed = 50

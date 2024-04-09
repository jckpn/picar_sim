from picar_sim import PicarSim
import objects

# TODO: randomise obstacles. add random obstacles to all scenes out of way of track


# 1. Keeping in lane driving along the straight section of the T-junction track, as
# shown in Fig. 1.
class Scene1(PicarSim):
    def __init__(self, **kwargs):
        super().__init__(
            picar=objects.Picar(center=(0, -10), angle=90),
            track=objects.tracks.Junction(),
            **kwargs,
        )


# 2. As (1), but driving as normal if pedestrians or other objects are on the side of
# (but not in) the road, as shown in Fig. 2.
class Scene2(Scene1):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_objects([objects.obstacles.Wood(center=(-50, -10))])

import numpy as np
from objects.base import SimulatorObject


class TrackMaterial(SimulatorObject):
    def __init__(self, center):
        super().__init__(
            center,
            size=(1, 1),
            angle=0,
            color=(0, 0, 0),
            can_collide=False,
        )


# wooden block, placeholder for actual obstacles
class Wood(SimulatorObject):
    def __init__(self, center):
        super().__init__(
            center,
            size=(10, 10),
            angle=np.random.randint(0, 360),
            image_path="objects/assets/obstacle.png",
            can_collide=True,
        )


class TrafficLight(SimulatorObject):
    def __init__(self, center, state="red"):
        super().__init__(
            center,
            size=(10, 10),
            angle=0,
            image_path="objects/assets/obstacle.png",
            can_collide=True,
        )

        self.set_state(state)

    def set_state(self, state):
        assert state in ["red", "green"]

        self.state = state
        self.image.fill((255, 80, 80) if state == "red" else (30, 200, 30))

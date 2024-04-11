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
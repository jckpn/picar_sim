from objects.base import SimulatorObject


class TrackMaterial(SimulatorObject):
    def __init__(self, center):
        super().__init__(
            center,
            size=(1, 1),
            angle=0,
            image_path=None,
            can_collide=False,
        )

# wooden block, placeholder for actual obstacles
class Wood(SimulatorObject):
    def __init__(self, center):
        super().__init__(
            center,
            size=(10, 10),
            angle=0,
            image_path="objects/assets/obstacle.png",
            can_collide=False,
        )

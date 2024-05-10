from sprites.base import SimulatorObject


class TrackMaterial(SimulatorObject):
    def __init__(self, center):
        super().__init__(
            center,
            size=(2, 2),
            direction=0,
            color=(255, 0, 255),
            can_collide=False,
        )
    
    def render(self, *args):
        pass  # too many, slows down sim
from sprites.base import SimulatorObject


class Obstacle(SimulatorObject):
    def __init__(self, center, size=(5, 5)):
        super().__init__(
            center,
            size=size,
            color=(255, 0, 255),
        )

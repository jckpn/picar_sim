from objects.base import SimulatorObject


class Obstacle(SimulatorObject):
    def __init__(self, center, size=(5, 5)):
        super().__init__(
            center,
            size=size,
            angle=0,
            image_path="objects/assets/obstacle.png",
            can_collide=True,
        )

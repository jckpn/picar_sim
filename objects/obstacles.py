from objects.base import SimulatorObject


class Wood(SimulatorObject):
    def __init__(
        self,
        center=(0, 0),
        size=(10, 10),
        direction=0,
        image_path="assets/obstacle.png",
    ):
        super().__init__(center, size, direction, image_path)

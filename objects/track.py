from objects import SimulatorObject


class Track(SimulatorObject):
    def __init__(
        self,
        center=(0, 0),
        size=(300, 164),
        direction=0,
        image_path="assets/track_oval.png",
    ):
        super().__init__(center, size, direction, image_path)

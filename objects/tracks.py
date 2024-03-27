from objects.base import SimulatorObject


class Track(SimulatorObject):
    def __init__(
        self,
        center=(0, 0),
        size=(300, 164),
        direction=0,
        *args,
        **kwargs,
    ):
        super().__init__(center, size, direction, *args, **kwargs)


class Oval(Track):
    def __init__(self):
        super().__init__(image_path="assets/track_oval.png")


class Figure8(Track):
    def __init__(self):
        super().__init__(image_path="assets/track_figure8.png")


class Junction(Track):
    def __init__(self):
        super().__init__(image_path="assets/track_junction.png")

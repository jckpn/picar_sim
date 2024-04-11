from objects.base import SimulatorObject


class Track(SimulatorObject):
    def __init__(self, center=(0, 0), size=(220, 110), image_path=None):
        super().__init__(center, size, angle=0, image_path=image_path)


class Oval(Track):
    def __init__(self):
        super().__init__(image_path="objects/assets/track_oval.png")


class Figure8(Track):
    def __init__(self):
        super().__init__(image_path="objects/assets/track_figure8.png")


class Junction(Track):
    def __init__(self):
        super().__init__(image_path="objects/assets/track_junction.png")

from objects.base import SimulatorObject


class GreenLight(SimulatorObject):
    def __init__(self, center):
        super().__init__(center, size=(5, 5), direction=0)

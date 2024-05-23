from picar_sim.objects.base_object import Object


class GreenLight(Object):
    def __init__(self, center):
        super().__init__(center, size=(5, 5), direction=0)

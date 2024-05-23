from picar_sim.objects.base_object import Object


class RightSign(Object):
    def __init__(self, center):
        super().__init__(center, size=(5, 5), direction=0, color=(255, 0, 255))
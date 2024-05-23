from picar_sim.objects.base_object import Object


class Obstacle(Object):
    def __init__(self, center, size=(5, 5)):
        super().__init__(
            center,
            size=size,
            color=(255, 0, 255),
        )

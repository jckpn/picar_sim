from picar_sim.objects.base_object import Object


class Track(Object):
    def __init__(self, image_path, center=(0, 0), size=(300, 150)):
        super().__init__(center=center, size=size, direction=0, image_path=image_path)
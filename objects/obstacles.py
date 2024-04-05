from objects.base_object import BaseObject


class Wood(BaseObject):
    def __init__(
        self,
        center=(0, 0),
        size=(10, 10),
        direction=0,
        image_path="objects/assets/obstacle.png",
        can_collide=False,
    ):
        super().__init__(center, size, direction, image_path, can_collide)

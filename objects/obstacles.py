from objects.base import SimObject


class Wood(SimObject):
    def __init__(
        self,
        center=(0, 0),
        size=(10, 10),
        direction=0,
        image_path="objects/assets/obstacle.png",
        collision_radius=5,
    ):
        super().__init__(center, size, direction, image_path, collision_radius)

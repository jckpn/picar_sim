from objects.base import SimulatorObject


class TrafficLight(SimulatorObject):
    def __init__(self, center, state="red"):
        super().__init__(center, size=(5, 5), angle=0)

        assert state in ["red", "green"]
        self.set_state(state)

    def set_state(self, state):
        self.state = state
        self.image.fill((255, 80, 80) if state == "red" else (30, 200, 30))

from .grid_state import GridState


class GridStateController:
    def __init__(self, state_size=30, state_range=60):
        self.state = GridState(size=30, obstacle_interval)

    def predict_from_state(self, state):  # override in controller subclass
        raise NotImplementedError

    def predict_sim(self, picar, env):  # for use in simulation
        self.state.observe_sim(picar, env, range=60)
        return self.predict_from_state(self.state)

    def predict(self, image):  # for use on actual car
        self.state.observe_real(image)
        return self.predict_from_state(self.state)

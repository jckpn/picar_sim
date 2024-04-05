import numpy as np
from picar_sim import PicarSim
from objects import obstacles

test_targets = [
    (50, 50),
    (20, 20),
    (18, -13),
    (33, -3),
    (25, 17),
    (9, 42),
    (-41, 23),
    (13, 25),
    (-20, 49),
    (30, 13),
    (7, -50),
    (-50, 10),
    (-15, 45),
    (-31, 21),
    (-23, -17),
    (35, 33),
    (-32, -27),
    (-8, 46),
    (-26, -18),
    (-41, 7),
    (-4, -43),
    (33, -43),
    (-30, -24),
    (-44, 25),
    (37, 48),
    (-43, 26),
    (36, -3),
    (-27, -20),
    (27, -43),
    (-7, -43),
    (25, -28),
    (37, 16),
    (-7, 3),
    (-37, 45),
    (34, -33),
    (-28, -49),
    (45, 1),
    (0, -6),
    (33, -38),
    (-19, -28),
    (-45, 20),
    (-10, -31),
    (-16, 6),
    (-26, 31),
    (38, -41),
    (36, -17),
    (6, 7),
    (36, -39),
    (-1, -9),
    (-34, 1),
    (23, 13),
    (29, -50),
    (15, -41),
    (15, -40),
    (-10, 28),
    (-43, 0),
    (-4, 39),
    (33, -35),
    (-14, -35),
    (47, 41),
    (48, -27),
    (-44, 28),
    (49, 42),
    (11, -31),
    (-27, -45),
    (-9, -5),
    (13, -18),
    (47, 35),
    (13, 22),
    (22, -45),
    (-42, 44),
    (19, 31),
    (1, 3),
    (-47, -38),
    (24, -10),
    (28, -17),
    (41, 3),
    (-15, 6),
    (44, 21),
    (-37, -30),
    (0, 34),
    (-14, -48),
    (-19, -30),
    (-3, -50),
    (37, 40),
    (7, 41),
    (22, 38),
    (28, -38),
    (16, -39),
    (-29, -22),
    (32, 0),
    (21, 12),
    (-13, 21),
    (42, 23),
    (12, -35),
    (38, 23),
    (-7, -49),
    (-17, -10),
    (-23, 33),
    (30, -19),
    (3, -28),
    (49, -38),
]


class NeuroTargetController:
    def __init__(self, hidden_size: int, weights=None):
        self.targets = []

        # we'll write the model from scratch since it's actually faster than tf for this
        # (i.e. small model with lots of single inferences)
        self.input_size = 2
        self.hidden_size = hidden_size
        self.output_size = 1

        if weights is not None:
            self.set_weights(weights)
        else:
            self.init_weights()

        self.training = False

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def model(self, x):
        x = np.append(x, 1)  # add bias
        x = np.dot(x, self.weights[0])  # hidden layer
        x = self.sigmoid(x)  # activation function
        x = np.append(x, 1)  # add bias
        x = np.dot(x, self.weights[1])
        x = self.sigmoid(x)
        return x

    def get_relative_targets(self, picar):
        relative_targets = self.targets - picar.center

        # rotate targets pos by -picar.angle
        angle = np.radians(-picar.angle)
        rotation_matrix = np.array(
            [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
        )
        relative_targets = np.array(
            [np.dot(rotation_matrix, t) for t in relative_targets]
        )

        return relative_targets

    def get_controls(self, picar):
        if len(self.targets) == 0:
            return 0, 0

        # need next target and one after it, so it can learn to chain targets
        relative_targets = self.get_relative_targets(picar)[:1]
        inputs = relative_targets.flatten() / 100  # normalise
        # np.clip(inputs, -1, 1, out=inputs)  # clip so really far targets don't mess up the model
        throttle = 1  # fixed full-speed throttle
        steer = self.model(inputs)[0]

        if not self.training:
            # this is also called during benchmark, don't want to call it twice
            self.check_if_target_reached(picar)

        return throttle, steer

    def check_if_target_reached(self, picar):
        if len(self.targets) == 0:
            return False

        if np.linalg.norm(picar.center - self.targets[0]) < 5:
            self.targets.pop(0)
            return True

        return False

    def set_weights(self, weights):
        self.weights = weights.copy()

    def init_weights(self):
        weights = [
            np.random.randn(self.input_size + 1, self.hidden_size),
            np.random.randn(self.hidden_size + 1, self.output_size),
        ]
        self.set_weights(weights)
        return weights

    def train(
        self,
        generations=100,
        population=100,
        init_lr=0.2,
        lr_decay=0.99,
        previews=True,
    ):
        self.training = True  # disable repeated target checks

        best_weights = self.weights  # initial weights (random by default, or pre-set)
        best_score = -np.inf

        lr = init_lr

        for g in range(generations):
            for p in range(population):
                # mutation
                species_mutations = [
                    np.random.randn(self.input_size + 1, self.hidden_size) * lr,
                    np.random.randn(self.hidden_size + 1, self.output_size) * lr,
                ]
                species_weights = [
                    best_weights[0] + species_mutations[0],
                    best_weights[1] + species_mutations[1],
                ]
                self.set_weights(species_weights)

                # test species
                species_score = self.benchmark()
                if species_score > best_score:
                    best_weights = species_weights.copy()
                    best_score = species_score

            # preview best species from this generation
            print(f"{g=}, {lr=:.3f}, {best_score=:.3f} ")
            self.set_weights(best_weights)
            self.benchmark(graphics=previews)

            # decay lr and population size exponentially
            lr *= lr_decay

        print(f"Best score: {best_score}")
        return best_weights

    def benchmark(self, time_per_target=10, graphics=False):
        sim = PicarSim(
            controller=self, speed_multiplier=4.0
        )  # create new sim with controller
        # show where targets are
        for t in test_targets:
            sim.add_obstacle(obstacles.Wood(center=t, size=(10, 10)))

        self.targets = test_targets.copy()

        score = 0.0
        time_left = time_per_target

        while time_left > 0:
            sim.loop()
            time_left -= 1 / sim.update_rate

            if graphics:
                sim.render()

            # reward facing target
            # next_target = self.get_relative_targets(sim.picar)[0]
            # a, o = next_target
            # angle = np.arctan2(o, a) * 180 / np.pi + 90
            # score -= np.abs(angle) * 0.001

            # reward reaching target
            if self.check_if_target_reached(sim.picar):
                time_left = time_per_target  # reset time limit
                score += 100 + 10 * time_left  # bonus for reaching target fast

                # # punish facing away from next target
                # next_target = self.get_relative_targets(sim.picar)[0]
                # a, o = next_target
                # angle = np.arctan2(o, a) * 180 / np.pi + 90
                # score -= np.abs(angle)

        # penalise distance to next target
        score -= np.linalg.norm(self.targets[0] - sim.picar.center)

        return score


if __name__ == "__main__":
    controller = NeuroTargetController(hidden_size=8)
    w = controller.train(init_lr=0.5, population=5000, previews=True)
    print(w)

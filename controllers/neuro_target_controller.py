import numpy as np
import main


class NeuroTargetController:
    def __init__(self, targets=[]):
        self.targets = targets

        # we'll write the model from scratch since it's actually faster than tf for this
        # (i.e. small model with lots of single inferences)
        self.input_num = 4
        self.hidden_num = 4
        self.output_num = 1
        self.init_weights()
        # self.set_weights(
        #     [
        #         np.array(
        #             [
        #                 [-4.05098262, 0.85425943, 4.99821611, -5.78502261],
        #                 [13.31044329, 0.81642658, -4.83351228, 2.01551118],
        #                 [1.61241551, -5.90434606, -0.25223213, 0.66830244],
        #                 [5.63508525, 1.29050874, 5.13137729, -9.52674633],
        #                 [1.94691, 0.32688074, 4.42739479, 7.62345313],
        #             ],
        #         ),
        #         np.array(
        #             [
        #                 [7.71077746],
        #                 [-2.40848012],
        #                 [3.55834757],
        #                 [0.28492701],
        #                 [-8.64543073],
        #             ]
        #         ),
        #     ]
        # )

        self.last_outputs = np.array([1, 0.5])

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

    def get_controls(self, picar):
        if len(self.targets) == 0:
            return 0, 0

        # need next target and one after it, so it can learn to chain targets
        relative_targets = (self.targets - picar.center)[:2]
        inputs = relative_targets.flatten() / 100  # normalise
        throttle = 1  # fixed throttle
        steer = self.model(inputs)[0]

        self.check_if_target_reached(picar)

        return throttle, steer

    def check_if_target_reached(self, picar):
        if len(self.targets) == 0:
            return

        if np.linalg.norm(picar.center - self.targets[0]) < 5:
            self.targets.pop(0)

    def set_weights(self, weights):
        self.weights = weights.copy()

    def init_weights(self):
        weights = [
            np.zeros((self.input_num + 1, self.hidden_num)),
            np.zeros((self.hidden_num + 1, self.output_num)),
        ]
        self.set_weights(weights)
        return weights

    def train(
        self,
        species=1000,
        generations=1000,
        init_lr=0.5,
    ):
        best_weights = self.init_weights()
        best_score = -np.inf

        for g in range(generations):
            # decay lr exponentially
            lr = init_lr * (1 - g / generations) ** 2

            for s in range(species):
                # mutation
                species_mutations = [
                    np.random.randn(self.input_num + 1, self.hidden_num) * lr,
                    np.random.randn(self.hidden_num + 1, self.output_num) * lr,
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

            print(f"{g=}, {lr=:.3f}, {best_score=:.3f} ")

        print(f"Best score: {best_score}")
        return best_weights

    def benchmark(self, time_per_target=10, dt=0.1):
        self.targets = [
            (-10, 10),
            (10, 20),
            (-20, 30),
            (-30, 40),
            (-50, 0),
            (-50, -50),
            (50, -50),
            (50, 50),
            (-50, 50),
        ]
        start_targets_len = len(self.targets)

        main.picar = main.objects.Picar()  # reset picar (TODO: picar.reset() ?)

        score = 0.0
        targets_reached = 0
        time_left = time_per_target

        while len(self.targets) > 0 and time_left > 0:
            main.sim_loop(self, dt=dt)
            time_left -= dt

            # reward reaching targets quickly
            if len(self.targets) < start_targets_len - targets_reached:
                score += 100  # + 10 * time_left
                time_left = time_per_target
                targets_reached += 1

        # penalise distance to next target
        score -= np.linalg.norm(main.picar.center - self.targets[0])

        return score


if __name__ == "__main__":
    controller = NeuroTargetController()
    w = controller.train()
    print(w)

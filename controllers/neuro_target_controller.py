import numpy as np
import main


class NeuroTargetController:
    def __init__(self, picar):
        self.picar = picar

        # we'll write the model from scratch since it's actually faster than tf for this
        # (i.e. small model with lots of single inferences)
        self.input_num = 6
        self.output_num = 2
        self.hidden_num = 10

        self.weights = [
            np.zeros([self.input_num + 1, self.hidden_num]),
            np.zeros([self.hidden_num + 1, self.output_num]),
        ]

        self.last_outputs = [1, 0.5]

        self.targets = []

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

    def get_controls(self):
        if len(self.targets) == 0:
            return 0, 0

        # need next target and one after it, so it can learn to chain targets
        relative_targets = (self.targets - self.picar.center)[:2]
        inputs = np.concatenate([relative_targets.flatten() / 100, self.last_outputs])
        throttle, steer = self.model(inputs)

        self.check_if_target_reached()

        return throttle, steer

    def check_if_target_reached(self):
        if len(self.targets) == 0:
            return

        if np.linalg.norm(self.picar.center - self.targets[0]) < 5:
            self.targets.pop(0)


def train(species=1000, generations=1000):
    controller = NeuroTargetController(main.picar)

    lr = 1.0

    best_weights = controller.weights.copy()
    best_score = -np.inf

    for generation_idx in range(generations):
        lr *= 0.95
        print(f"generation: {generation_idx}, {lr=}")
        for species_idx in range(species):
            weights = best_weights.copy()

            for layer in weights:
                mutation = np.random.randn(*layer.shape) * lr
                layer += mutation

            score = benchmark(controller)

            if score > best_score:
                best_weights = weights.copy()
                best_score = score
                print(f"new best score: {best_score}")


benchmark_targets = [np.random.rand(2) * 40 - 20 for _ in range(100)]


def benchmark(controller):
    controller.targets = benchmark_targets.copy()
    og_targets_len = len(controller.targets)

    main.picar = main.objects.Picar()  # reset picar
    controller.picar = main.picar

    for _ in range(1000):
        main.sim_loop(controller, dt=0.1)

    score = 1000 * (og_targets_len - len(controller.targets))
    score -= np.linalg.norm(controller.picar.center - controller.targets[0])

    return score


if __name__ == "__main__":
    train()

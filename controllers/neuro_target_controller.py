import numpy as np
import main
import tensorflow as tf


model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Dense(4, input_shape=(4,), activation="relu"),
        tf.keras.layers.Dense(4, activation="relu"),
        tf.keras.layers.Dense(2, activation="sigmoid"),
    ]
)


class NeuroTargetController:
    def __init__(self, picar):
        self.picar = picar

        self.targets = []

    def get_controls(self, dt):
        if len(self.targets) == 0:
            return 0, 0

        # need next target and one after it, so it can learn to chain targets
        relative_targets = (self.targets - self.picar.center)[:2]

        inputs = tf.expand_dims(relative_targets.flatten(), axis=0)
        throttle, steer = model.predict(inputs, verbose=0)[0]

        return throttle, steer


def train():
    controller = NeuroTargetController(main.picar)

    # generate random co-ords within bounds of environment
    for _ in range(2):
        target = np.random.rand(2) * 100 - 50
        controller.targets.append(target)

    for _ in range(1000):
        main.sim_loop(controller, dt=0.1)


if __name__ == "__main__":
    train()

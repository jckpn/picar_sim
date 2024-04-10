import scenes
import controllers


def main():
    sim = scenes.Scene2(
        # TODO: spawn picar at random locations/angles to train network how to recover
        # /without/ training it to veer off track by itself
        controller=controllers.GridNeuralController(),
        speed_multiplier=1.0,
    )
    # sim.set_perspective(sim.picar)  # makes manual driving easier
    sim.loop()


if __name__ == "__main__":
    main()

import scenes
from shared.model import MoeController
from controllers import GridCaptureController


TRAINING = False


def main():
    sim = scenes.Scene4(
        controller=MoeController(smoothing=0.0)
        if not TRAINING
        else GridCaptureController(),
        speed_multiplier=1,
        controller_interval=0.05,
    )

    if TRAINING:
        sim.set_perspective(sim.picar)
        sim.random_picar_position()

    sim.start_loop()


if __name__ == "__main__":
    main()

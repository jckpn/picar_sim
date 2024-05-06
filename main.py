import scenes
from shared.model import MoeController
from controllers import GridCaptureController, MouseController


# TODO
# - test different networks for different tasks + inference times so we can make table
#   for evaluation section:
#    - recovery out of 10 random positions, # occurences leaving lane, etc.
#    - inference time, and test difference inference times to get goal time


SCENE = scenes.Scene11
MAX_SPEED = 50
RECORD = False


def main():
    if RECORD:
        sim = SCENE(
            controller=GridCaptureController(base_controller=MouseController()),
            controller_interval=0.01,  # capture more data
        )
        sim.set_perspective(sim.picar)  # makes driving easier
    else:
        sim = SCENE(
            controller=MoeController(smoothing=0.0, print_state=True),
            controller_interval=0.05,  # simulate real-world delay
        )

    # sim.random_picar_position()  # to train or test recovery ability

    sim.picar.set_max_speed(MAX_SPEED)
    sim.start_loop()


if __name__ == "__main__":
    main()

import scenes
from shared.model import MoeController
from controllers import GridCaptureController, MouseController


# TODO
# - get data for:
#   - left turn at junction (scene 10) -- turns at intersection are not tested!
#   - right turn at junction (scene 11)
#   - wait at intersections (for scenes 8 and 9)
# - make gating function work, and test it
# - add and test interventions for obstacles and traffic lights
# - test different networks for different tasks + inference times so we can make table
#   for evaluation section:
#    - recovery out of 10 random positions, # occurences leaving lane, etc.
#    - inference time, and test difference inference times to get goal time


SCENE = scenes.Scene8
MAX_SPEED = 50
RECORD = False


def main():
    if RECORD:
        sim = SCENE(
            controller=GridCaptureController(base_controller=MouseController()),
            controller_interval=0.01,  # capture more per second
        )
        sim.set_perspective(sim.picar)  # makes driving easier
    else:
        sim = SCENE(
            controller=MoeController(smoothing=0.5),
            controller_interval=0.1,  # simulate real-world delay
        )

    # sim.random_picar_position()  # to train or test recovery ability

    sim.picar.set_max_speed(MAX_SPEED)
    sim.start_loop()


if __name__ == "__main__":
    main()
